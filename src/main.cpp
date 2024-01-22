#include <iostream>
#include <opencv2/opencv.hpp>

void harrisCornerDetection(const cv::Mat& image, int windowSize, double k, double threshold) {
    // Convert the image to grayscale
    cv::Mat gray;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);

    // Compute image gradients using Sobel operators
    cv::Mat Ix, Iy;
    cv::Sobel(gray, Ix, CV_64F, 1, 0, 3);
    cv::Sobel(gray, Iy, CV_64F, 0, 1, 3);

    // Compute products of gradients
    cv::Mat Ixx = Ix.mul(Ix);
    cv::Mat Iyy = Iy.mul(Iy);
    cv::Mat Ixy = Ix.mul(Iy);

    // Apply Gaussian blur to the products of gradients
    int kernelSize = 5;
    cv::GaussianBlur(Ixx, Ixx, cv::Size(kernelSize, kernelSize), 0);
    cv::GaussianBlur(Iyy, Iyy, cv::Size(kernelSize, kernelSize), 0);
    cv::GaussianBlur(Ixy, Ixy, cv::Size(kernelSize, kernelSize), 0);

    // Calculate the Harris corner response
    cv::Mat detM = Ixx.mul(Iyy) - Ixy.mul(Ixy);
    cv::Mat traceM = Ixx + Iyy;
    cv::Mat harrisResponse = detM - k * traceM.mul(traceM);

    // Normalize the Harris response to a scale of 0 to 255
    cv::normalize(harrisResponse, harrisResponse, 0, 255, cv::NORM_MINMAX, CV_64F);

    // Apply threshold to detect corners
    cv::Mat corners = cv::Mat::zeros(image.size(), CV_8UC1);
    corners.setTo(255, harrisResponse > threshold * harrisResponse.max());

    // Display the original and result images
    cv::imshow("Original Image", image);
    cv::imshow("Harris Corner Detection Result", corners);
    cv::waitKey(0);
    cv::destroyAllWindows();
}

int main() {
    // Load the image
    cv::Mat originalImage = cv::imread("path_to_your_image.jpg");

    if (originalImage.empty()) {
        std::cerr << "Error: Could not read the image." << std::endl;
        return -1;
    }

    // Apply Harris Corner Detection
    harrisCornerDetection(originalImage, 3, 0.04, 0.01);

    return 0;
}
