
#include <iostream>
#include <fstream>
#include <iomanip>
#include "railway_graph.hpp"
#include "json.hpp"
#include <filesystem>

namespace fs = std::filesystem;
using namespace std;
using json = nlohmann::json;

int main() {
    cout << "Program started...";

    if (!fs::exists("data")) {
        fs::create_directory("data");
        cout << "Created 'data' directory.";
    } else {
        cout << "'data' directory already exists.";
    }

    ifstream i("data/uttarakhand_railway.json");
    if (!i.is_open()) {
        cerr << "Failed to open input JSON file: data/uttarakhand_railway.json\n";
        return 1;
    }

    json railway_data;
    i >> railway_data;
    cout << "Input JSON loaded successfully.\n";

    RailwayGraph graph(railway_data);

    int choice;
    cout << "Enter your choice:\n1. Visualize Entire Graph\n2. Visualize Path (source to destination)\nChoice: ";
    cin >> choice;

    string start, end;
    if (choice == 2) {
        cout << "Enter source station code: ";
        cin >> start;
        cout << "Enter destination station code: ";
        cin >> end;
    }

    if (choice == 1) {
        json all = graph.full_graph_json();
        ofstream full_out("data/uttarakhand_full_graph.json");
        full_out << setw(4) << all << endl;
        cout << "Full graph data saved.";
    } else if (choice == 2) {
        json dfs_result = graph.dfs(start, end);
        ofstream dfs_out("data/uttarakhand_dfs_result.json");
        dfs_out << setw(4) << dfs_result << endl;

        json dijkstra_distance_result = graph.dijkstra(start, end, true);
        ofstream dijkstra_distance_out("data/uttarakhand_dijkstra_distance_result.json");
        dijkstra_distance_out << setw(4) << dijkstra_distance_result << endl;

        json dijkstra_time_result = graph.dijkstra(start, end, false);
        ofstream dijkstra_time_out("data/uttarakhand_dijkstra_time_result.json");
        dijkstra_time_out << setw(4) << dijkstra_time_result << endl;

        cout << "Path data saved.";
    }

    return 0;
}
 
