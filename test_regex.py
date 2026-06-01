import re

line = ':::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/create_project.py" id="create_client":::'
repo_token = 'foundry-samples'
pattern = rf'\(~/{repo_token}[^)]*\)|source="~/{repo_token}[^"]*"'
print(f"Pattern: {pattern}")
print(f"Line: {line}")
m = re.findall(pattern, line)
print(f"Matches: {m}")

# Also test azureai-samples pattern
line2 = ':::code language="python" source="~/azureai-samples-main/scenarios/evaluate/test.py" id="test":::'
repo_token2 = 'azureai-samples'
pattern2 = rf'\(~/{repo_token2}[^)]*\)|source="~/{repo_token2}[^"]*"'
m2 = re.findall(pattern2, line2)
print(f"azureai-samples matches: {m2}")
