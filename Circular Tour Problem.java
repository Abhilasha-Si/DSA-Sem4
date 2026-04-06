class PetrolPump {
    int petrol, distance;

    PetrolPump(int petrol, int distance) {
        this.petrol = petrol;
        this.distance = distance;
    }
}

class CircularTour {
    public static int findStart(PetrolPump[] pumps) {
        int total = 0, curr = 0, start = 0;

        for (int i = 0; i < pumps.length; i++) {
            int diff = pumps[i].petrol - pumps[i].distance;

            total += diff;
            curr += diff;

            if (curr < 0) {
                start = i + 1;
                curr = 0;
            }
        }

        return (total >= 0) ? start : -1;
    }
}