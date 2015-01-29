TWITTERFILE=../trowser3/oneyear.json
GRAPHFILE=social_graph.json

#cliques.pkl: $(GRAPHFILE)
all: mongosetup

clean:
	rm social_graph.pkl cliques.json clique_graph_edges.json twitter_user_id.json twitter_user_id_sorted.json user_dict.pkl twitter_user_players.json mongocliques mongoedges mongoimport mongotwitter

# This will generate a large number of ValueErrors. Don't worry about them
social_graph.pkl: $(GRAPHFILE)
	python -OO readgraph.py $(GRAPHFILE)

user_dict.pkl: twitter_user_id_sorted.json
	python -OO make_user_dict.py twitter_user_id_sorted.json

cliques.json: $(TWITTERFILE) social_graph.pkl findcliques.py user_dict.pkl
	python -OO findcliques.py social_graph.pkl $(TWITTERFILE) user_dict.pkl > cliques.json

clique_graph_edges.json: make_clique_graph.py cliques.json
	python -OO make_clique_graph.py cliques.json > clique_graph_edges.json

twitter_user_id.json:
	python -OO fix_user_id.py $(TWITTERFILE) > twitter_user_id.json


twitter_user_id_sorted.json: twitter_user_id.json
	python -OO popdate.py twitter_user_id.json | sort -n - | cut -f 2- -d ' '  - > twitter_user_id_sorted.json

twitter_user_players.json: twitter_user_id_sorted.json popats.py
	python -OO popats.py twitter_user_id_sorted.json > twitter_user_players.json

mongotwitter: twitter_user_players.json
	mongoimport --drop --db trowser --collection twitter twitter_user_players.json
	touch mongotwitter

mongocliques: cliques.json 
	mongoimport --drop --db trowser --collection cliques cliques.json  # preprocessed w/ my script
	touch mongocliques

mongoedges:  clique_graph_edges.json
	mongoimport --drop --db trowser --collection edges clique_graph_edges.json  # preprocessed w/ my script
	touch mongoedges

mongoimport: mongotwitter mongocliques mongoedges 
	touch mongoimport

mongosetup: mongoimport
	mongo localhost:27017/trowser mongosetup
	touch mongosetup

