#include <iostream>
#include <fstream>
#include <unordered_map>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#define PORT 12345
#define BUFFER_SIZE 1024

// Function to load users from users.txt into a hash map
std::unordered_map<std::string, std::string> load_users(const std::string& filename) {
    std::unordered_map<std::string, std::string> users;
    std::ifstream file(filename);
    std::string line, username, password;

    if (!file) {
        std::cerr << "Error opening users file." << std::endl;
        exit(1);
    }

    while (std::getline(file, line)) {
        size_t delimiter_pos = line.find(':'); // Find the colon separator
        if (delimiter_pos != std::string::npos) {
            username = line.substr(0, delimiter_pos);
            password = line.substr(delimiter_pos + 1);
            users[username] = password;
        }
    }

    return users;
}


void handle_client(int client_socket, const std::unordered_map<std::string, std::string>& users) {
    char buffer[BUFFER_SIZE];
    memset(buffer, 0, BUFFER_SIZE);
    
    // Request username
    std::string message = "Enter username: ";
    send(client_socket, message.c_str(), message.size(), 0);
    recv(client_socket, buffer, BUFFER_SIZE, 0);
    std::string username(buffer);
    
    // Request password
    memset(buffer, 0, BUFFER_SIZE);
    message = "Enter password: ";
    send(client_socket, message.c_str(), message.size(), 0);
    recv(client_socket, buffer, BUFFER_SIZE, 0);
    std::string password(buffer);
    
    // Authentication
    if (users.find(username) != users.end() && users.at(username) == password) {
        message = "Welcome to the server";
    } else {
        message = "Authentication failed";
    }
    send(client_socket, message.c_str(), message.size(), 0);
    
    close(client_socket);
}

int main() {
    int server_socket, client_socket;
    sockaddr_in server_address{}, client_address{};
    socklen_t client_len = sizeof(client_address);
    
    // Load users from file
    std::unordered_map<std::string, std::string> users = load_users("users.txt");
    
    // Create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        std::cerr << "Error creating socket." << std::endl;
        return 1;
    }
    
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);
    
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        std::cerr << "Binding failed." << std::endl;
        return 1;
    }
    
    listen(server_socket, 5);
    std::cout << "Server listening on port " << PORT << std::endl;
    
    while (true) {
        client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_len);
        if (client_socket < 0) {
            std::cerr << "Error accepting connection." << std::endl;
            continue;
        }
        std::cout << "Client connected." << std::endl;
        handle_client(client_socket, users);
    }
    
    close(server_socket);
    return 0;
}