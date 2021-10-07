#!/usr/bin/env python3

import os
import re
import sys
import json
import argparse
import requests

'''
This script is to be run only after original repo has been transferred from the original org to
the new org and porked back to the original org.

Input:
- repo name
- original org
- new org
- personal access token (via environment variable)

Major things the script does:
1. retrieve all releases from new org using GitHub REST api `releases` endpoint
2. save the releases as JSON under the `releases` folder as backup
3. iterate all releases, one by one
4. for each release
   - if it's a WFPM package release, download WFPM assets and save them under the `releases` folder as backup
   - if it's a WFPM package release, update release body to add additional information, such as wfpm package uri
   - create a new release in the forked repo at the original org
   - if it's a WFPM package release, upload the downloaded WFPM assets
'''


def download_file(url, outdir):
    local_filename = url.split('/')[-1]
    os.makedirs(outdir, exist_ok=True)
    local_file = os.path.join(outdir, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_file


def upload_asset(asset, release_id, repo, org, github_pat):
    url = f"https://uploads.github.com/repos/{org}/{repo}/releases/{release_id}/assets"
    data = open(asset, 'rb').read()
    params = {
        'name': os.path.basename(asset)
    }

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/octet-stream",
        "Authorization": f"token {github_pat}",
    }

    res = requests.post(
        url,
        headers=headers,
        params=params,
        data=data
    )

    if res.status_code != 201:
        sys.exit(
            f"Asset upload failed with status code: {res.status_code}. Additional info: {res.text}")
    else:
        print(f"Asset upload successful: {asset}")


def get_releases(repo, org):
    headers = {"accept": "application/vnd.github.v3+json"}

    url = f"https://api.github.com/repos/{org}/{repo}/releases"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        releases = json.loads(res.text)
        return releases

    else:
        raise Exception(f"Unable to retrieve releases from: {url}")


def create_release(source_release, repo, org, github_pat, backup_dir):
    target_commitish = source_release['target_commitish']
    tag_name = source_release['tag_name']

    release_body = source_release.get('body')

    assets = source_release.get('assets')
    asset_files = []

    if assets:  # WFPM package release has additional assets
        pkg_name = tag_name.split('.')[0]
        pkg_ver = '.'.join(tag_name.split('.')[1:])
        if re.match(r'^v.+', pkg_ver):
            pkg_ver = pkg_ver.replace('v', '', 1)

        if not re.match(r'\* Package URI: ', release_body):  # add only when needed
            # URI: github.com/icgc-argo/icgc-25k-azure-transfer/score-data-transfer@0.4.0
            additional_release_note = f"* Package URI: `github.com/{org.lower()}/{repo}/{pkg_name}@{pkg_ver}`"
            release_body = f"{release_body}\n{additional_release_note}"

        # download assets
        for asset in assets:
            local_asset_file = download_file(
                asset['browser_download_url'], os.path.join(backup_dir, tag_name))
            asset_files.append(local_asset_file)

    release_to_create = {
        'tag_name': tag_name,
        'name': source_release['name'],
        'body': release_body,
        'prerelease': source_release['prerelease'],
        'draft': source_release['draft'],
    }

    if re.match(r'^[a-f0-9]{40}$', target_commitish):
        release_to_create['target_commitish'] = target_commitish

    # now create the release
    print(f"Releasing: {org}/{repo}/{tag_name}")
    release_create_url = f"https://api.github.com/repos/{org}/{repo}/releases"
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_pat}",
    }

    res = requests.post(
        release_create_url,
        headers=headers,
        json=release_to_create
    )

    release_id = None
    if res.status_code != 201:
        sys.exit(
            f"Release creation failed with status code: {res.status_code}. Additional info: {res.text}")
    else:
        release_id = res.json()['id']

    # now upload release assets if any
    for asset in asset_files:
        upload_asset(asset, release_id, repo, org, github_pat)

    print(f"Released: {org}/{repo}/{tag_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Script to re-create GitHub releases based on source repo after forking')
    parser.add_argument('-r', '--repo', type=str,
                        help='Repository name', required=True)
    parser.add_argument('-f', '--forked-org', type=str,
                        help='Forked repository organization', required=True)
    parser.add_argument('-s', '--source-org', type=str, default='icgc-argo-workflows',
                        help='Source repository organization')
    args = parser.parse_args()

    github_pat = os.environ.get('GITHUB_PAT')
    if not github_pat:
        sys.exit(
            'Please provide GitHub Personal Access Token as environment variable: GITHUB_PAT')

    # create source org/repo dir to keep release data (could serve as backup)
    backup_dir = os.path.join('releases', args.source_org, args.repo)
    os.makedirs(backup_dir, exist_ok=True)

    releases = get_releases(args.repo, args.source_org)
    with open(os.path.join(backup_dir, 'releases.json'), 'w') as f:
        f.write(json.dumps(releases, indent=2))

    if not releases:
        print(
            f"No release found for https://github.com/{args.source_org}/{args.repo}")
        sys.exit()

    for release in reversed(releases):
        create_release(release, args.repo, args.forked_org,
                       github_pat, backup_dir)


if __name__ == "__main__":
    main()
