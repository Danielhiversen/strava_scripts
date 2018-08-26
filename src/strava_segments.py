import stravalib
import time
from queue import PriorityQueue

from stravalib.util.limiter import SleepingRateLimitRule

POS = [61.40114, 5.72880, 61.52709, 6.12294,] # Your home region
N = 10

def main(segment_id):
    client = stravalib.client.Client(access_token='37d4400d9157c0d7b0237e5a5568d9af41272462',
                                     rate_limiter=SleepingRateLimitRule(priority='low'))

    pos = POS
    main_seg = client.get_segment(segment_id=segment_id)
    priority_queue = PriorityQueue()
    ids = []

    j = 0
    for num in range(0, N, 1):
        print(num)
        for k in range(num):
            for l in range(num):
                for i in range(2):
                    pos = [POS[0] + (POS[2] - POS[0])*l/num + i*(POS[2] - POS[0])/2,
                           POS[1] + (POS[3] - POS[1])*k/num + i*(POS[2] - POS[0])/2,
                           POS[0] + (POS[2] - POS[0])*(l+1)/num + i*(POS[2] - POS[0])/2,
                           POS[1] + (POS[3] - POS[1])*(k+1)/num + i*(POS[2] - POS[0])/2]
                    for min_cat in range(6):
                        o = 0
                        while True:
                            o += 1
                            try:
                                segs = client.explore_segments(pos,
                                                               activity_type='running',
                                                               min_cat=min_cat,
                                                               max_cat=min_cat+1)
                            except:
                                time.sleep(min(o, 10))
                                continue
                            break
                        for seg in segs:
                            j += 1
                            if seg.id in ids:
                                continue
                            ids.append(seg.id)
                            w = round(abs(main_seg.average_grade - seg.avg_grade)) + abs(main_seg.distance.num - seg.distance.num)/5000.0
                            priority_queue.put((w, seg.id))

    print(j, len(ids))
    print()
    print()

    print(main_seg)
    print(main_seg.id, main_seg.average_grade, main_seg.distance.num)

    print()
    print()

    for k in range(10):
        closest_seg = client.get_segment(segment_id=priority_queue.get()[1])
        print()
        print(closest_seg)
        print(closest_seg.id, closest_seg.average_grade, closest_seg.distance.num)

if __name__ == "__main__":
    for segment_id in [5616829, 5616873, 5616884, 5616903, 5715125,
     12578648, 9891572, 8350594, 9915722, 10388926, 12623964, 5417462, 13384408]:
        main(segment_id=segment_id)
