"""
Test: use same code path as find-snippets.py but only for articles/foundry
to debug why foundry-samples refs aren't being found.
"""
import re
import os
import sys
sys.path.insert(0, '.')
from utilities import helpers as h
from utilities import gh_auth as a
from utilities import config as cfg_module

repo = a.connect_repo("MicrosoftDocs/azure-ai-docs")

repos_config = cfg_module.get_repositories()
repo_configs = {}
for repo_key, repo_config in repos_config.items():
    repo_configs[repo_key] = {
        "repo_token": repo_config.get("snippet_repo", repo_config["repo"]),
        "owners": repo_config["team"]
    }

exclude_dirs = cfg_module.get_exclude_directories()

print(f"repo_configs:")
for k, v in repo_configs.items():
    print(f"  {k}: repo_token={v['repo_token']}")

# Only search articles/foundry with include_subdirs=True (same as main script)
print(f"\nGetting all contents from articles/foundry...")
contents = h.get_all_contents(repo, "articles/foundry", "main", exclude_dirs)
print(f"Found {len(contents)} files")

md_files = [c for c in contents if c.type == "file" and c.name.endswith(".md")]
print(f"Of which {len(md_files)} are .md files")

match_count = 0
for content_file in md_files[:20]:  # limit to first 20 for speed
    file = os.path.basename(content_file.path)
    try:
        file_content = content_file.decoded_content
    except Exception as e:
        print(f"Error reading {content_file.path}: {e}")
        continue
    lines = file_content.decode().splitlines()
    
    for line_num, line in enumerate(lines, start=1):
        for repo_key, config in repo_configs.items():
            repo_token = config["repo_token"]
            az_branch = f"{repo_token}-main"
            match_snippet = re.findall(
                rf'\(~/{repo_token}[^)]*\)|source="~/{repo_token}[^"]*"', line
            )
            if match_snippet:
                match_count += 1
                path, ref_file, branch, m, name = h.cleanup_matches(match_snippet[0])
                print(f"  MATCH in {content_file.path}:{line_num}")
                print(f"    repo_key={repo_key}, token={repo_token}, branch={branch}, az_branch={az_branch}")
                print(f"    branch==az_branch: {branch == az_branch}")

print(f"\nTotal matches found: {match_count}")
