
#pragma once
#include <string>
#include <unordered_map>
#include <vector>
#include "json.hpp"

using json = nlohmann::json;

class RailwayGraph {
public:
    RailwayGraph(const json& data);
    json dfs(const std::string& start, const std::string& end);
    json dijkstra(const std::string& start, const std::string& end, bool by_distance);
    json full_graph_json();
private:
    json railway_data;
};
