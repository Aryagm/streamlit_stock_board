#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <stdexcept>

// Stock Data Structure
struct StockData
{
    double price;        // Price of the stock
    unsigned int volume; // Trading volume of the stock

    // Constructor to initialize StockData with price and volume
    StockData(double p, unsigned int v) : price(p), volume(v) {}
};

// Sentiment Score Structure
struct SentimentScore
{
    double score; // Sentiment score, representing market sentiment

    // Explicit constructor to prevent accidental conversions
    explicit SentimentScore(double s) : score(s) {}
};

// Base Analyzer Class
class BaseAnalyzer
{
public:
    // Pure virtual function to enforce implementation in derived classes
    virtual std::string analyzeTrend() = 0;
};

// Stock Analyzer Class
class StockAnalyzer : public BaseAnalyzer
{
    std::vector<StockData> stockData; // Container for stock data
    SentimentScore sentimentScore;    // Sentiment score associated with the stock data

public:
    // Constructor to initialize StockAnalyzer with stock data and sentiment score
    StockAnalyzer(const std::vector<StockData> &data, const SentimentScore &score)
        : stockData(data), sentimentScore(score) {}

    // Function to calculate the average price of the stock
    double calculateAveragePrice()
    {
        double sum = 0;
        for (const auto &data : stockData)
        {
            sum += data.price; // Summing up the prices
        }
        // Returning the average price, or 0 if no data is available
        return stockData.empty() ? 0 : sum / stockData.size();
    }

    // Overridden function to analyze and predict the stock trend
    std::string analyzeTrend() override
    {
        double avgPrice = calculateAveragePrice(); // Calculate average price
        // Predicting trend based on sentiment score and price comparison
        if (sentimentScore.score > 0 && avgPrice > stockData.back().price)
        {
            return "Likely to Rise";
        }
        else if (sentimentScore.score < 0 && avgPrice < stockData.back().price)
        {
            return "Likely to Fall";
        }
        else
        {
            return "Uncertain Trend";
        }
    }
};

// Function to read stock data from a file
std::vector<StockData> readStockData(const std::string &filename, double &sentimentScore)
{
    std::vector<StockData> stockData; // Vector to store the read stock data
    std::ifstream inFile(filename);   // File stream for reading data

    // Check if file opened successfully
    if (!inFile.is_open())
    {
        throw std::runtime_error("Error opening " + filename);
    }

    std::string line; // String to hold each line read from the file
    // Reading file line by line
    while (std::getline(inFile, line))
    {
        // Check if the line contains sentiment score
        if (line.rfind("Sentiment Score:", 0) == 0)
        {
            // Extracting sentiment score from the line
            std::istringstream(line.substr(17)) >> sentimentScore;
        }
        else
        {
            // Parsing stock data (price and volume) from the line
            std::istringstream ss(line);
            double price;
            unsigned int volume;
            ss >> price >> volume;
            // Adding the parsed data to the stockData vector
            stockData.emplace_back(price, volume);
        }
    }
    return stockData; // Returning the populated stock data vector
}

int main()
{
    try
    {
        std::string inputFilename = "stock_data.txt";         // Input file name
        std::string outputFilename = "prediction_result.txt"; // Output file name
        double sentimentScore;                                // Variable to store sentiment score

        // Reading stock data from file
        std::vector<StockData> stockData = readStockData(inputFilename, sentimentScore);

        // Creating an instance of StockAnalyzer with the read data
        StockAnalyzer analyzer(stockData, SentimentScore(sentimentScore));
        // Analyzing the trend based on the stock data and sentiment score
        std::string trendPrediction = analyzer.analyzeTrend();

        // Opening a file stream for writing the prediction result
        std::ofstream outFile(outputFilename);
        if (!outFile.is_open())
        {
            // If the file cannot be opened, throw an exception
            throw std::runtime_error("Error opening " + outputFilename);
        }
        // Writing the predicted trend to the output file
        outFile << "Predicted Trend: " << trendPrediction << std::endl;
        outFile.close(); // Closing the file stream

        // Displaying a user-friendly message to the console
        std::cout << "Analysis complete. Prediction written to " << outputFilename << std::endl;
        std::cout << "Predicted Trend: " << trendPrediction << std::endl;
    }
    catch (const std::runtime_error &e) // Catching any runtime errors
    {
        // Displaying the error message to the console
        std::cerr << "An error occurred: " << e.what() << std::endl;
        return 1; // Returning 1 indicates an error occurred
    }

    return 0; // Returning 0 indicates successful execution
}

// Comments:
// - The program demonstrates the use of classes, objects, and methods (OOP concepts).
// - Encapsulation is shown through the use of private data members in the StockAnalyzer class.
// - Inheritance and polymorphism are demonstrated with the BaseAnalyzer class and its virtual function.
// - Exception handling is used for file operations.
// - User-friendly messages are provided for better interaction.
// - The code is formatted for clarity and includes comments for understanding.
// - The design allows for easy modification and reuse of the StockAnalyzer class.

// Additional Comments (Ion know why this is a seperate section :/ ):
// - The program is structured to demonstrate key concepts in C++ programming, including object-oriented programming, file I/O, exception handling, and data structures.
// - The use of std::vector and std::string simplifies dynamic data management.
// - The program is designed to be modular, with separate functions for reading data and analyzing trends, enhancing readability and maintainability.
// - Exception handling ensures the program can gracefully handle unexpected situations, such as file access issues.
// - The code includes user-friendly console output to inform the user of the program's progress and results.
