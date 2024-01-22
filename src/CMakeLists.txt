cmake_minimum_required(VERSION 3.12)
project( Ex2 )

MESSAGE( STATUS "------------------" ${OpenCV_INCLUDE_DIRS} )

#
find_package( OpenCV REQUIRED )

#
add_executable(Ex2
	harris.cpp

	main.cpp
)


target_include_directories( Ex2
	PRIVATE 	.
			${OpenCV_INCLUDE_DIRS}
)

target_link_libraries( Ex2 
	${OpenCV_LIBS} 
)
