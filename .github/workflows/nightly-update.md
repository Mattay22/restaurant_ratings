---
on: 
  schedule:
    # Run daily at 3am UTC, all days except Saturday and Sunday
    - cron: "0 3 * * 1-5"
  workflow_dispatch:
  stop-after: +48h # workflow will no longer trigger after 48 hours

timeout_minutes: 15


permissions:
  contents: write  # Required so the agent can review the code in the repository
  issues: write   # Required so the agent can create issues for accessibility problems
  actions: read
  checks: read
  statuses: read

tools:
  github:
    allowed: [
        get_file_contents,
        trigger_workflow
    ]
  claude:
    allowed:
      WebFetch:
      WebSearch:
---

# Nighty Update

## Job Description
Checkout ${{ github.repository }} repository and run this script tools/get_data.py and upon completion run this script tools/map_gen2.py