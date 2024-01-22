/*
 *      Author: alexanderb
 */

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

struct Derivatives {
	Mat Ix;
	Mat Iy;
	Mat Ixy;
};

struct pointData { 
    float cornerResponse;

    Point point;
};

struct by_cornerResponse { 
    bool operator()(pointData const &left, pointData const &right) { 
        return left.cornerResponse > right.cornerResponse;
    }
};

class Harris {
public:
    Harris(Mat img, float k, int filterRange, bool gauss);
	vector<pointData> getMaximaPoints(float percentage, int filterRange, int suppressionRadius);

private:
	Mat convertRgbToGrayscale(Mat& img);
	Derivatives computeDerivatives(Mat& greyscaleImg);	
	Derivatives applyMeanToDerivatives(Derivatives& dMats, int filterRange);
	Derivatives applyGaussToDerivatives(Derivatives& dMats, int filterRange);
	Mat computeHarrisResponses(float k, Derivatives& intMats);

	Mat computeIntegralImg(Mat& img);
	Mat meanFilter(Mat& intImg, int range);
	Mat gaussFilter(Mat& img, int range);

private:
	Mat m_harrisResponses;
};

class Util {
public:
	static void DisplayImage(Mat& img);
	static void DisplayMat(Mat& img);
	static void DisplayPointVector(vector<Point> vp);

	static Mat MarkInImage(Mat& img, vector<pointData> points, int radius);
};