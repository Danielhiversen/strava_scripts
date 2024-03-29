import stravalib
import time
from queue import PriorityQueue

from stravalib.util.limiter import SleepingRateLimitRule

POS = [59.694999, 9.871651, 59.940306, 10.474260]  # Your home region
POS = [59.701668, 9.933852, 59.798844, 10.243552]  # Your home region
N = 10


def main(segment_id):
    client = stravalib.client.Client(access_token='1a310aaf6d7b13664943ed2e91af8289e1b07320',
                                     rate_limiter=SleepingRateLimitRule(priority='low'))

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
                        o = 1
                        while True:
                            try:
                                segs = client.explore_segments(pos,
                                                               activity_type='running',
                                                               min_cat=min_cat,
                                                               max_cat=min_cat+1)
                            except:
                                time.sleep(min(o, 120))
                                o += 10
                                continue
                            break
                        for seg in segs:
                            j += 1
                            if seg.id in ids:
                                continue
                            ids.append(seg.id)
                            # w = round(abs(main_seg.average_grade - seg.avg_grade)) + abs(main_seg.distance.num - seg.distance.num)/5000.0
                            w = round(abs((main_seg.elevation_high.num - main_seg.elevation_low.num) - seg.elev_difference.num)) + abs(main_seg.distance.num - seg.distance.num)/5000.0
                            priority_queue.put((w, seg.id))

    print("--------")
    print(j, len(ids))
    print()
    print()

    print(main_seg)
    print(main_seg.id, main_seg.average_grade, main_seg.distance.num)

    print()
    print()

    for _ in range(10):
        closest_seg = client.get_segment(segment_id=priority_queue.get()[1])
        print()
        print(closest_seg)
        print(closest_seg.id, closest_seg.average_grade, closest_seg.distance.num)


if __name__ == "__main__":
    # SEGMENTS = [5616829, 5616873, 5616884, 5616903, 5715125, 12578648, 9891572, 8350594, 9915722, 10388926, 12623964, 5417462, 13384408]
    SEGMENTS = [24913052, 24913068, 24913082, 24913098, 24913122, 24913144]
    for segment_id in SEGMENTS:
        main(segment_id=segment_id)
