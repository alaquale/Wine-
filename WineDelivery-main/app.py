from flask import Flask, render_template, jsonify, request
from Agents import *
from Problems import *
import json

app = Flask(__name__)

result = None
main_obj = None
started = False
Finished = True

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/Italy_routing')
def ItalyEnv():
    return render_template('ItalyRoute.html')

@app.route('/Italy_routing/start',methods=['POST'])
def ItalyStart():
    if started == False:
        data = json.loads(request.data.decode('utf-8'))
        source = data['source']
        target = data['target']
        algorithm = data['algorithm']

        if algorithm == 'bfs':
            X = ItalyBFSAgent(initial_state=source,goal_state=target)
            result = X.run()
        elif algorithm == 'dfs':
            X = ItalyDFSAgent(initial_state=source,goal_state=target)
            result = X.run()
        elif algorithm == 'lds':
            X = ItalyDLSAgent(initial_state=source,goal_state=target,max_depth=10)
            result = X.run()
        elif algorithm == 'ids':
            X = ItalyIDSAgent(initial_state=source,goal_state=target)
            result = X.run()
        elif algorithm == 'greedy':
            X = ItalyGreedyAgent(initial_state=source,goal_state=target)
            result = X.run()
        elif algorithm == 'astar':
            X = ItalyAStarAgent(initial_state=source,goal_state=target)
            result = X.run()
        elif algorithm == 'ucs':
            X = ItalyUCSAgent(initial_state=source,goal_state=target)
            result = X.run()

        print('xxxxxx Algoritmo utilizzato : '+algorithm+' xxxxxxxxxxx',result,'\n\n')
        return jsonify({
            'goal' : result
        })
app.debug = False
app.run(threaded=True)
