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

For each repository to be migrated, please follow these steps:
0. Make sure to complete and release all currently in-development packages
1. Transfer the ownership of the repository from the original organization to the new organization (https://github.com/icgc-argo-workflows)
2. Fork the same repo from the new organization back to the original organization
3. Since forking at step 2 does not create releases, run the `release-duplicator.py` script to create all releases for
   the forked repo at the original organization so that the releases are the same as what in the repo under the new organization
4. In the forked repo under the original organization, add archive note in README.md and commit. Archive note may look like:
   ```
   NOTE: this repository is archived to support workflow reproducibility. Active development
   continues at: <url to the new repo>
   ```
5. Archive the forked repo under the original organization, the archived repo must be maintained for as long as
   needed to maintain reproducibility of workflow versions ran in ARGO production.
6. Continue to maintain all existing docker images registered under either the original GitHub organization or under quay.io.


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

