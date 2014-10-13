TWITTERFILE=oneyear.json
GRAPHFILE=social_graph.json

#cliques.pkl: $(GRAPHFILE)
all: mongosetup

clean:
	rm social_graph.pkl cliques.json clique_graph_edges.json twitter_user_id.json twitter_user_id_sorted.json

# This will generate a large number of ValueErrors. Don't worry about them
social_graph.pkl:
	python -OO readgraph.py $(GRAPHFILE)

cliques.json: $(TWITTERFILE) social_graph.pkl findcliques.py
	python -OO findcliques.py social_graph.pkl $(TWITTERFILE) > cliques.json

clique_graph_edges.json: make_clique_graph.py cliques.json
	python -OO make_clique_graph.py cliques.json > clique_graph_edges.json

twitter_user_id.json:
	python -OO fix_user_id.py $(TWITTERFILE) > twitter_user_id.json


twitter_user_id_sorted.json: twitter_user_id.json
	python -OO popdate.py twitter_user_id.json | sort -n - | cut -f 2- -d ' '  - > twitter_user_id_sorted.json

mongotwitter: twitter_user_id_sorted.json
	mongoimport --drop --db trowser --collection twitter twitter_user_id_sorted.json

mongocliques: cliques.json 
	mongoimport --drop --db trowser --collection cliques cliques.json  # preprocessed w/ my script

mongoedges:  clique_graph_edges.json
	mongoimport --drop --db trowser --collection edges clique_graph_edges.json  # preprocessed w/ my script

mongoimport: mongotwitter mongocliques mongoedges 

mongosetup: mongoimport
	mongo localhost:27017/trowser mongosetup.js

