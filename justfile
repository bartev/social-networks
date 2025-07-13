# Settings
set ignore-comments := true
set quiet := false

# List commands
_list:
	@echo "📋 Available commands:"
	@just --list --unsorted


# page rank (pr_hits is better)
[group: "streamlit-meh"]
page_rank:
    streamlit run apps/page_rank.py

# basic_viz
[group: "streamlit-meh"]
basic_viz:
    streamlit run apps/basic_viz.py

# dynamic_interactions
[group: "streamlit"]
dynamic_interactions:
    streamlit run apps/dynamic_interactions.py

# interactive_viz
[group: "streamlit"]
interactive_viz:
    streamlit run apps/interactive_viz.py

# pr_hits (Page rank + HITS)
[group: "streamlit"]
pr_hits:
    streamlit run apps/pr_hits.py

# two_viz (Matplotlib + pyviz)
[group: "streamlit"]
two_viz:
    streamlit run apps/two_viz.py
