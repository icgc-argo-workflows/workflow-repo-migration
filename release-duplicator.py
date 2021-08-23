#!/usr/bin/env python3

'''
Tis script is to be run only after original repo has been transferred from the original org to
the new org and porked back to the original org.

Input:
- repo name
- original org
- new org
- personal access token (via environment variable)

Major things the script does:
1. retrieve all releases from new org using GitHub REST api `releases` endpoint
2. iterate all releases, one by one
3. for each release
   - if it's a WFPM package release, download WFPM assets
   - if it's a WFPM package release, update release body to add additional information, such as wfpm package uri
   - create a new release in the original org
   - if it's a WFPM package release, upload the downloaded WFPM assets
'''
