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
[group: "streamlit module 3"]
dynamic_interactions:
    streamlit run apps/dynamic_interactions.py

# interactive_viz
[group: "streamlit module 3"]
interactive_viz:
    streamlit run apps/interactive_viz.py

# pr_hits (Page rank + HITS)
[group: "streamlit module 3"]
pr_hits:
    streamlit run apps/pr_hits.py

# two_viz (Matplotlib + pyviz)
[group: "streamlit module 3"]
two_viz:
    streamlit run apps/two_viz.py

[group: "streamlit module 4"]
pref-attach:
    streamlit run apps/mod_4_barabasi_albert_graph.py

# format notebook (black) (nbqa)
[group: "python"]
black-nb fname:
    nbqa black {{fname}}

# lint/fix (ruff) (nbqa)
[group: "python"]
ruff-nb fname:
    nbqa ruff {{fname}} --fix
