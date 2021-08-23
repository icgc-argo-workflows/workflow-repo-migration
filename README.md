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

1. There is also a fallback plan if things happened not as expected. The fallback plan is to transfer the
   original repo back to the original organization.
2. The migration process should be brief, typically should be under 10 minutes per repo.
3. After migration, for any released version of the workflow, it can be run properly using either the original
   git url or the new one. And in either case, the workflow code and docker images used should be exactly the same.
4. Original repositories must be archived and maintained (not to be deleted) from the original organization.
5. Original docker images must be maintained at the original github organization (either ghcr.io or quay.io
   depending on the origina of the docker image).
6. WFPM packages released under the original repositories will continue to be available to be imported, just like
   how it works before the migration.


## Workflow source repositories to be migrated

| Original repo                         |   Original org        | Migration status |  New repo | New org |
|---------------------------------------|-----------------------|------------------|-----------|----------|
| [dna-seq-processing-wfs](https://github.com/icgc-argo/dna-seq-processing-wfs)  | icgc-argo  | To be done |   |  |
| [nextflow-data-processing-utility-tools](https://github.com/icgc-argo/nextflow-data-processing-utility-tools) | icgc-argo | To be done|  |   |
| [data-processing-utility-tools](https://github.com/icgc-argo/data-processing-utility-tools)  |  icgc-argo  | To be done |     |   |
| [dna-seq-processing-tools](https://github.com/icgc-argo/dna-seq-processing-tools)  | icgc-argo  | To be done |    |  |
| [data-qc-tools-and-wfs](https://github.com/icgc-argo/data-qc-tools-and-wfs)  | icgc-argo  | To be done |   |  |
| [gatk-tools](https://github.com/icgc-argo/gatk-tools)                        | icgc-argo  | To be done |   |  |


## Repository migration standard operating procedure (SOP)

For each repository to be migrated, please follow these steps:
1. Transfer the ownership of the repository from the original organization to the new organization (https://github.com/icgc-argo-workflows)
2. Fork the same repo from the new organization back to the original organization
3. Since forking at step 2 does not create releases, run the `release-duplicator.py` script to create all releases for
   the forked repo at the original organization so that the releases are the same as what in the repo under the new organization
4. In the forked repo under the original organization, add archive note in README.md and commit. Archive note may look like:
   ```
   NOTE: this repository is archived to support workflow reproducibility. Active development continues at: <url to the new repo>
   ```
5. Archive the forked repo under the original organization, the archived repo must be maintained for as long as
   needed to maintain reproducibility of workflow versions ran in ARGO production.
6. Note that GitHub repo ownership transfer does not affect docker images created from those repos. No work needed
   for docker registries (neither ghcr.io nor quay.io), all docker images registered under the original organization
   continue to exist and must be maintained to ensure all workflows to run properly, at this point the same workflow
   can be run from both old and new repo. 
