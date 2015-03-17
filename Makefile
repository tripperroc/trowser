TWITTERFILE=data/oneyear.json
GRAPHFILE=data/social_graph.json
TWITTERDATA=data/
PROCESSFILE=processfile/
#cliques.pkl: $(GRAPHFILE)
all: mongosetup

clean:
	rm $(TWITTERDATA)social_graph.pkl $(TWITTERDATA)cliques.json $(TWITTERDATA)clique_graph_edges.json $(TWITTERDATA)twitter_user_id.json $(TWITTERDATA)twitter_user_id_sorted.json $(TWITTERDATA)user_dict.pkl $(TWITTERDATA)twitter_user_players.json mongocliques mongoedges mongoimport mongotwitter

# This will generate a large number of ValueErrors. Don't worry about them
$(TWITTERDATA)social_graph.pkl: $(GRAPHFILE)
	python -OO $(PROCESSFILE)readgraph.py $(GRAPHFILE)

$(TWITTERDATA)user_dict.pkl: $(TWITTERDATA)twitter_user_id_sorted.json
	python -OO $(PROCESSFILE)make_user_dict.py $(TWITTERDATA)twitter_user_id_sorted.json

$(TWITTERDATA)cliques.json: $(TWITTERFILE) $(TWITTERDATA)social_graph.pkl $(PROCESSFILE)findcliques.py $(TWITTERDATA)user_dict.pkl
	python -OO $(PROCESSFILE)findcliques.py $(TWITTERDATA)social_graph.pkl $(TWITTERFILE) $(TWITTERDATA)user_dict.pkl > $(TWITTERDATA)cliques.json

$(TWITTERDATA)clique_graph_edges.json: $(PROCESSFILE)make_clique_graph.py $(TWITTERDATA)cliques.json
	python -OO $(PROCESSFILE)make_clique_graph.py $(TWITTERDATA)cliques.json > $(TWITTERDATA)clique_graph_edges.json

$(TWITTERDATA)twitter_user_id.json:
	python -OO $(PROCESSFILE)fix_user_id.py $(TWITTERFILE) > $(TWITTERDATA)twitter_user_id.json


$(TWITTERDATA)twitter_user_id_sorted.json: $(TWITTERDATA)twitter_user_id.json
	python -OO $(PROCESSFILE)popdate.py $(TWITTERDATA)twitter_user_id.json | sort -n - | cut -f 2- -d ' '  - > $(TWITTERDATA)twitter_user_id_sorted.json

$(TWITTERDATA)twitter_user_players.json: $(TWITTERDATA)twitter_user_id_sorted.json $(PROCESSFILE)popats.py
	python -OO $(PROCESSFILE)popats.py $(TWITTERDATA)twitter_user_id_sorted.json > $(TWITTERDATA)twitter_user_players.json

mongotwitter: $(TWITTERDATA)twitter_user_players.json
	mongoimport --drop --db trowser --collection twitter $(TWITTERDATA)twitter_user_players.json
	touch mongotwitter

mongocliques: $(TWITTERDATA)cliques.json
	mongoimport --drop --db trowser --collection cliques $(TWITTERDATA)cliques.json  # preprocessed w/ my script
	touch mongocliques

mongoedges:  $(TWITTERDATA)clique_graph_edges.json
	mongoimport --drop --db trowser --collection edges $(TWITTERDATA)clique_graph_edges.json  # preprocessed w/ my script
	touch mongoedges

mongoimport: mongotwitter mongocliques mongoedges
	touch mongoimport

mongosetup: mongoimport
	mongo localhost:27017/trowser mongosetup
	touch mongosetup

