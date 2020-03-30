def get_distances(height, distances):
        #List of pixcels where there is trash ( Randomly choosen Number )
        list_of_distances = []

        pixel_length = 37/height

        for distance in distances:
                distanceInCM = float(distance) * pixel_length
                list_of_distances.append(distanceInCM)

        return list_of_distances
