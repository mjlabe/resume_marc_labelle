# Resume content guidelines

## Resume variants

- `content/staff.yaml` is the broad staff-engineer resume. Balance backend, platform, embedded, mobile, and delivery work for senior individual-contributor roles.
- `content/staff-backend.yaml` is the backend-oriented staff resume. Prioritize APIs, data flows, infrastructure, security, testing, and service reliability; mention embedded or mobile work only when it clarifies the backend system.
- `content/lead.yaml` is the engineering-lead resume. Prioritize people leadership, cross-functional execution, mentoring, contractor management, support ownership, architecture, and delivery outcomes while retaining enough technical detail to establish hands-on credibility.

## Content rules

- Keep employment titles, employers, dates, achievements, and technologies factual and consistent across variants unless a variant needs a different level of emphasis.
- Do not use the biometric product's project name in resume copy unless the user explicitly asks for it. Describe it generically as a biometric data-collection product or platform.
- Favor concise, outcome-oriented bullets that begin with a strong verb. Keep consultant bullets at or below 127 characters unless the user directs otherwise.
- Do not add spiritual, aura, or other non-technical framing to the biometric product work.
- Preserve existing user edits and avoid unrelated content changes.

## Validation

- After editing resume content, parse every changed YAML file before reporting completion:

  ```sh
  ruby -e 'require "yaml"; ARGV.each { |file| YAML.load_file(file); puts "#{file}: valid YAML" }' content/staff.yaml content/staff-backend.yaml content/lead.yaml
  ```
- Run `make build-static` only when a PDF rebuild is requested. Generated PDFs are build artifacts and should not be edited directly.
