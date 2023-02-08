# Description
<!--- Briefly describe the changes included in this pull request  --->

### Closes #...  <!-- edit if this PR closes an Issue -->

---
## Test Results

<!--- Please test the following in a built docker image.  --->


### Validation Test

#### BAM

Case 1 - test type: <!-- e.g. fail on invalid, fail on empty, pass on valid, etc.  -->
- input file(s):
   ```
   path/to/input
   ```
- command: 
  ```
  <command used>
  ```
- output: 
  ```
  path/to/output OR output-message
  ```

#### VCF
Case 1 - test: <!-- e.g. fail on invalid, fail on empty, pass on valid, etc.  -->
- input file(s):
   ```
   path/to/input
   ```
- command: 
  ```
  <command used>
  ```
- output: 
  ```
  path/to/output OR output-message
  ```

Case 2 - test: <!-- e.g. pass on valid, fail on invalid, fail on empty, etc.  -->
- input file(s):
   ```
   path/to/input
   ```
- command: 
  ```
  <command used>
  ```
- output: 
  ```
  path/to/output OR output-message
  ```
--- 
### Checksum Test

Case 1 - test: <!-- e.g. pass on valid checksum, fail on invalid checksum, checksum generation, etc.  -->
- input file(s):
   ```
   path/to/input
   ```
- command: 
  ```
  <command used>
  ```
- output: 
  ```
  path/to/output OR output-message
  ```

---

# Checklist
<!--- Please read each of the following items and confirm by replacing the [ ] with a [X] --->

### File Commits

- [ ] This PR **does *NOT* contain** Protected Health Information [(PHI)](https://ohrpp.research.ucla.edu/hipaa/). A repo may ***need to be deleted*** if such data is uploaded. <br> Disclosing PHI is a ***major problem***[^1] - Even ***a small leak can be costly***[^2].
  
- [ ] This PR **does *NOT* contain** germline genetic data[^3], RNA-Seq, DNA methylation, microbiome or other molecular data[^4].

[^1]: [UCLA Health reaches $7.5m settlement over 2015 breach of 4.5m patient records](https://healthitsecurity.com/news/ucla-health-reaches-7.5m-settlement-over-2015-breach-of-4.5m)
[^2]: [The average healthcare data breach costs $2.2 million, despite the majority of breaches releasing fewer than 500 records.](https://www.ponemon.org/local/upload/file/Sixth%20Annual%20Patient%20Privacy%20%26%20Data%20Security%20Report%20FINAL%206.pdf)
[^3]: [Genetic information is considered PHI.](https://www.genome.gov/about-genomics/policy-issues/Privacy#:~:text=In%202013%2C%20as%20required%20by,genetic%20information%20for%20underwriting%20purposes.)
  [Forensic assays can identify patients with as few as 21 SNPs](https://www.sciencedirect.com/science/article/pii/S1525157817305962)
[^4]: [RNA-Seq](https://www.nature.com/articles/ng.2248), [DNA methylation](https://ieeexplore.ieee.org/document/7958619), [microbiome](https://www.pnas.org/doi/pdf/10.1073/pnas.1423854112), or other molecular data can be used to predict genotypes (PHI) and reveal a patient's identity.

- [ ] This PR **does *NOT* contain** other non-plain text files, such as: compressed files, images (*e.g.* `.png`, .`jpeg`), `.pdf`, `.RData`, `.xlsx`, `.doc`, `.ppt`, or other output files.

_&emsp; To automatically exclude such files using a [.gitignore](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files) file, see [here](https://github.com/uclahs-cds/template-base/blob/main/.gitignore) for example._

### Code Review Best Practices

- [ ] I have read the [code review guidelines](https://confluence.mednet.ucla.edu/display/BOUTROSLAB/Code+Review+Guidelines) and the [code review best practice on GitHub check-list](https://confluence.mednet.ucla.edu/display/BOUTROSLAB/Code+Review+Best+Practice+on+GitHub+-+Check+List).

- [ ] I have set up or verified the `main` branch protection rule following the [github standards](https://confluence.mednet.ucla.edu/pages/viewpage.action?spaceKey=BOUTROSLAB&title=GitHub+Standards#GitHubStandards-Branchprotectionrule) before opening this pull request.

- [ ] The name of the branch is meaningful and well formatted following the [standards](https://confluence.mednet.ucla.edu/display/BOUTROSLAB/Code+Review+Best+Practice+on+GitHub+-+Check+List), using [AD_username (or 5 letters of AD if AD is too long)]-[brief_description_of_branch].
  
- [ ] I have added the major changes included in this pull request to the `CHANGELOG.md` under the next release version or unreleased, and updated the date.

### Testing

- [ ] I have added unit tests for the new feature(s).

- [ ] I modified the integration test(s) to include the new feature.

- [ ] All new and previously existing tests passed locally and/or on the cluster.

- [ ] The docker image built successfully on the cluster.
