#!/usr/bin/python
import datetime

def load(filename="hackdiet_db.txt", alpha=0.1):
  print "Loading", filename

  # I. Load all rows with weight entry
  raw_db = []
  with open("hackdiet_db.csv") as f:
    for l in f:
      if l == "" or l[0] not in ["1","2"]: continue
      date, weight = l.split(",")[0:2]
      if weight != "":
        date = datetime.date(*map(int, date.split("-")))
        raw_db.append((date, float(weight)))
  assert len(raw_db) > 0, "Error: Database seems to be empty"
  raw_db.sort(key=lambda entry: entry[0])
  print "Loaded %s non-empty data entries." % len(raw_db)

  # II. Missing entries: interpolate weight between days
  db = []
  for (date0, weight0), (date1, weight1) in zip(raw_db[0:], raw_db[1:]):
    num_days = (date1-date0).days
    for d in range(num_days):
      f = d / float(num_days)
      date = date0 + datetime.timedelta(d)
      weight = (1.0-f)*weight0 + f*weight1
      db.append((date, weight))
  db.append(raw_db[-1]) # re-attach last day
  print "Created %s interpolated entries." % len(db)

  # III. Calculate moving average for each day
  avg_db = []
  avg = db[0][1]
  for date, weight in db:
    avg = alpha*weight + (1.0-alpha)*avg
    avg_db.append((date, weight, avg))

  return avg_db

def export(db, filename="hackdiet_db.txt"):
  print "Exporting:", filename

  with open(filename, "w+") as f:
    f.write("# date            weight           average\n")
    for date, weight, avg in db:
      f.write("%s\t%s\t%s\n" % (date, weight, avg))

if __name__ == "__main__":
  export(load())
