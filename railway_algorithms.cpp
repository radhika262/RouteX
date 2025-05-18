
#include "railway_graph.hpp"
#include <queue>
#include <unordered_set>
#include <limits>

using namespace std;

RailwayGraph::RailwayGraph(const json& data) {
    railway_data = data;
}

json RailwayGraph::dfs(const string& start, const string& end) {
    unordered_set<string> visited;
    vector<string> path;
    json result;

    function<bool(string)> dfs_helper = [&](string current) {
        visited.insert(current);
        path.push_back(current);
        if (current == end) return true;
        for (auto& conn : railway_data[current]["connections"]) {
            string next = conn["to"];
            if (!visited.count(next)) {
                if (dfs_helper(next)) return true;
            }
        }
        path.pop_back();
        return false;
    };

    dfs_helper(start);
    result["path"] = path;
    return result;
}

json RailwayGraph::dijkstra(const string& start, const string& end, bool by_distance) {
    unordered_map<string, int> dist;
    unordered_map<string, string> prev;
    auto cmp = [&](pair<int, string> a, pair<int, string> b) {
        return a.first > b.first;
    };
    priority_queue<pair<int, string>, vector<pair<int, string>>, decltype(cmp)> pq(cmp);

    for (auto& station : railway_data.items()) {
        dist[station.key()] = numeric_limits<int>::max();
    }
    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [curr_dist, curr] = pq.top(); pq.pop();
        if (curr == end) break;

        for (auto& conn : railway_data[curr]["connections"]) {
            string next = conn["to"];
            int weight = conn[by_distance ? "distance" : "time"];
            if (curr_dist + weight < dist[next]) {
                dist[next] = curr_dist + weight;
                prev[next] = curr;
                pq.push({dist[next], next});
            }
        }
    }

    vector<string> path;
    for (string at = end; !at.empty(); at = prev.count(at) ? prev[at] : "") {
        path.push_back(at);
        if (at == start) break;
    }
    reverse(path.begin(), path.end());
    return {{"path", path}, {"cost", dist[end]}};
}

json RailwayGraph::full_graph_json() {
    return railway_data;
}
