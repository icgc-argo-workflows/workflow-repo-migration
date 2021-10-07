# Migrate ARGO workflow source code repositories to under the new GitHub organization

We have decided to migrate all ARGO workflow source code repositories to a dedicated new
GitHub organization (https://github.com/icgc-argo-workflows) to make it easier to manage
ARGO workflow source code, coordinate development efforts and share the workflows with
broader cancer genomics and bioinformatics communities. The timing is also right as we have
largely finished processing ICGC 25K data using ARGO workflows and a large number of
developers from ARGO participating institutes are joining forces to develop more ARGO workflows.

To make the process more manageable, we will do the migration is multiple phases:
* first, a pilot phase includes repos under `icgc-argo` organization that are related to ARGO DNA alignment workflow
* second, the remaining workflow repos under `icgc-argo` organization
* third, workflow repos reside in GitHub organizations managed by different working groups


## Summary of objectives

After workflow source code repository migration, we'd like to make it no impact on running the workflows. This
is primarily to fulfill our commitment to workflow reproducibility. All versions of the ARGO workflows were used
to process production data must be reproducible, even after the source code repo migration.

* There is also a fallback plan if things happened not as expected. The fallback plan is to transfer the
  original repo back to the original organization.
* The migration process should be brief, typically should be under 10 minutes per repo.
* After migration, for any released version of the workflow, it can be run properly using either the original
  git url or the new one. And in either case, the workflow code and docker images used should be exactly the same.
* Original repositories must be archived and maintained (not to be deleted) from the original organization.
* Original docker images must be maintained at the original github organization (either ghcr.io or quay.io
  depending on the origina of the docker image).
* WFPM packages released under the original repositories will continue to be available to be imported, just like
  how it works before the migration.


## Repository migration standard operating procedure (SOP)

**Prerequisite**: the user executing the SOP needs to be owner of both source and target
GitHub organizations in order to initial repository transfer.

For each repository to be migrated, please follow these steps:

0. Make sure to complete and release all currently in-development packages
1. Transfer the ownership of the repository from the original organization to the new organization (https://github.com/icgc-argo-workflows)
2. Fork the same repo from the new organization back to the original organization
3. Fork might take some time although it looks completed quickly, pause for ~30 minutes
   before continuing
4. Since forking at step 2 does not create releases, run the `release-duplicator.py` script to create all releases for
   the forked repo at the original organization so that the releases are the same as what in the repo under the new organization. If you get error creating a release, you
   will need to delete the fork and start over from step 2 and pause longer at step 3.
5. Run `git add .` and `git commit` to backup releases and associated assets.
6. In the forked repo under the original organization, add archive note in README.md and commit. Archive note may look like:
   ```
   NOTE: this repository is archived to support workflow reproducibility. Active development
   continues at: <url to the new repo>
   ```
7. Archive the forked repo under the original organization, the archived repo must be maintained for as long as
   needed to maintain reproducibility of workflow versions ran in ARGO production.
8. Continue to maintain all existing docker images registered under either the original GitHub organization or under quay.io.


## One-time update before continue the development under the new GitHub organization

For each repository after migrated to under the new GitHub organization, please follow
these steps to complete a one-time update before normal WFPM package development process:

0. Make a fresh clone of the repository
1. On the main branch, edit configuration file, package metadata file, source code
scripts of all packages from old GitHub organization to the new organization. Here
is an example commit update the organization for two packages under the repository
`icgc-argo-workflows/demo-pkgs1`: https://github.com/icgc-argo-workflows/demo-pkgs1/commit/5d012d691a154f9b55281e178ea4cc29e5ee1b87. Example files to be updated:
  * `.wfpm`: WFPM project config file
  * `nextflow.config`: Nextflow config file
  * `<package-a>/pkg.json`: Package A metadata JSON file
  * `<package-a>/main.nf`: Package A entry point script
  * `<package-a>/tests/checker.nf`: Packge A test launcher script
  * `<package-b>/pkg.json`: Package B metadata JSON file
  * `<package-b>/main.nf`: Package B entry point script
  * `<package-b>/tests/checker.nf`: Packge B test launcher script
2. For each package, create a new version under the new organization:
 * assume the package name is `pkg-a` and the latest version is `1.2.3`, start a new
   version using `wfpm nextver pkg-a@1.2.3 1.2.3.1`. This will create a new branch
   `pkg-a@1.2.3.1` and make it the current branch.
 * then merge the update from main branch `git merge main`
 * continue as usual with: git push, create PR and merge PR. Do NOT release the
   package when merge the PR
3. repeat **step 2** until all WFPM packages in the repository are covered
4. switch to the main branch and run `git pull` to sync with the remote
5. run WFPM release command to release each of the new package version, eg,
   `wfpm release pkg-a@1.2.3.1` to release version `1.2.3.1` of `pkg-a`
6. repeat **step 5** until all new versions of all packages are released


## Workflow source repositories to be migrated

| Original repo                         |   Original org        | Migration status |  New repo | New org |
|---------------------------------------|-----------------------|------------------|-----------|----------|
| [dna-seq-processing-wfs](https://github.com/icgc-argo/dna-seq-processing-wfs)  | icgc-argo  | completed | [dna-seq-processing-wfs](https://github.com/icgc-argo-workflows/dna-seq-processing-wfs)  | icgc-argo-workflows |
| [nextflow-data-processing-utility-tools](https://github.com/icgc-argo/nextflow-data-processing-utility-tools) | icgc-argo | completed | [nextflow-data-processing-utility-tools](https://github.com/icgc-argo-workflows/nextflow-data-processing-utility-tools) | icgc-argo-workflows  |
| [data-processing-utility-tools](https://github.com/icgc-argo/data-processing-utility-tools)  |  icgc-argo  | completed |  [data-processing-utility-tools](https://github.com/icgc-argo-workflows/data-processing-utility-tools)   | icgc-argo-workflows  |
| [dna-seq-processing-tools](https://github.com/icgc-argo/dna-seq-processing-tools)  | icgc-argo  | completed |  [dna-seq-processing-tools](https://github.com/icgc-argo-workflows/dna-seq-processing-tools)  | icgc-argo-workflows |
| [data-qc-tools-and-wfs](https://github.com/icgc-argo/data-qc-tools-and-wfs)  | icgc-argo  | completed | [data-qc-tools-and-wfs](https://github.com/icgc-argo-workflows/data-qc-tools-and-wfs)  | icgc-argo-workflows |
| [gatk-tools](https://github.com/icgc-argo/gatk-tools)                        | icgc-argo  | completed | [gatk-tools](https://github.com/icgc-argo-workflows/gatk-tools)  | icgc-argo-workflows |
| [sanger-wgs-variant-calling](https://github.com/icgc-argo/sanger-wgs-variant-calling)                        | icgc-argo  | completed | [sanger-wgs-variant-calling](https://github.com/icgc-argo-workflows/sanger-wgs-variant-calling)   | icgc-argo-workflows |
| [sanger-wxs-variant-calling](https://github.com/icgc-argo/sanger-wxs-variant-calling)                        | icgc-argo  | completed | [sanger-wxs-variant-calling](https://github.com/icgc-argo-workflows/sanger-wxs-variant-calling)  | icgc-argo-workflows |
| [gatk-mutect2-variant-calling](https://github.com/icgc-argo/gatk-mutect2-variant-calling)                        | icgc-argo  | completed | [gatk-mutect2-variant-calling](https://github.com/icgc-argo-workflows/gatk-mutect2-variant-calling)  | icgc-argo-workflows |
| [variant-calling-tools](https://github.com/icgc-argo/variant-calling-tools)                        | icgc-argo  | completed | [variant-calling-tools](https://github.com/icgc-argo-workflows/variant-calling-tools)  | icgc-argo-workflows |
| [open-access-variant-filtering](https://github.com/icgc-argo/open-access-variant-filtering)                        | icgc-argo  | completed | [open-access-variant-filtering](https://github.com/icgc-argo-workflows/open-access-variant-filtering)  | icgc-argo-workflows |
| [icgc-argo-sv-copy-number](https://github.com/ICGC-ARGO-Structural-Variation-CN-WG/icgc-argo-sv-copy-number) | ICGC-ARGO-Structural-Variation-CN-WG  | to be completed |   | icgc-argo-workflows |
| [argo-qc-tools](https://github.com/icgc-argo-qc-wg/argo-qc-tools) | icgc-argo-qc-wg  | to be completed |   | icgc-argo-workflows |

