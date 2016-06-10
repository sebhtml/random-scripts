#!/usr/bin/env python3

import sys
import time
import argparse
from prettytable import PrettyTable

NSEC_PER_SEC = 1000000000

try:
    from babeltrace import TraceCollection
except ImportError:
    # quick fix for debian-based distros
    sys.path.append("/usr/local/lib/python%d.%d/site-packages" %
                    (sys.version_info.major, sys.version_info.minor))
    from babeltrace import TraceCollection


class TraceParser:
    def __init__(self, trace):
        self.trace = trace
        self.event_count = {}

    def ns_to_hour_nsec(self, ns):
        d = time.localtime(ns/NSEC_PER_SEC)
        return "%02d:%02d:%02d.%09d" % (d.tm_hour, d.tm_min, d.tm_sec,
                                        ns % NSEC_PER_SEC)

    def parse(self):
        # iterate over all the events

        debug = False

        phases = []

        enter_times = {}

        phase_deltas = {}

        # This only works with 1 thread -- it assumes that the
        # events are in the same thread.
        for event in self.trace.events:

            event_name = event.name
            event_time = event.timestamp

            if not event_name in self.event_count.keys():
                self.event_count[event_name] = 0

            self.event_count[event_name] += 1

            enter_suffix = "_enter"
            exit_suffix = "_exit"
            enter_success = len(event_name) - len(enter_suffix)
            exit_success = len(event_name) - len(exit_suffix)

            if event_name.find(enter_suffix) == enter_success:

                enter_times[event_name] = event_time
                base_name = event_name[:- len(enter_suffix)]

                if base_name not in phase_deltas:
                    phase_deltas[base_name] = []
                    phases.append(base_name)

            elif event_name.find(exit_suffix) == exit_success:
                base_name = event_name[:- len(exit_suffix)]

                enter_event_name = base_name + enter_suffix

                enter_time = 0

                delta = -1

                if enter_event_name in enter_times:
                    enter_time = enter_times[enter_event_name]
                    delta = event_time - enter_time

                    if debug:
                        print("ENTER %s %d" % (enter_event_name, enter_time))
                        print("EXIT %s %d" % (event_name, event_time))
                        print("DELTA %s %d" % (base_name, delta))

                    if base_name not in phase_deltas:
                        phase_deltas[base_name] = []

                    phase_deltas[base_name].append(delta)

        data = []
        for name in phases:

            deltas = phase_deltas[name]
            count = len(deltas)

            sorted(deltas)

            middle = int(count / 2)
            median = deltas[middle]

            data.append([name, count, median])

        table = PrettyTable()

        table.field_names = ["Phase", "Count", "MedianDelta(ns)"]
        table.align["Phase"] = "l"
        table.align["Count"] = "r"
        table.align["MedianDelta(ns)"] = "r"

        for row in data:
            table.add_row(row)

        print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Trace parser')
    parser.add_argument('path', metavar="<path/to/trace>", help='Trace path')
    args = parser.parse_args()

    traces = TraceCollection()
    handle = traces.add_traces_recursive(args.path, "ctf")
    if handle is None:
        sys.exit(1)

    t = TraceParser(traces)
    t.parse()

    for h in handle.values():
        traces.remove_trace(h)
