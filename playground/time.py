import time

# capture start time
start_time = time.time()

for i in range(1000):
  i = i + 1

# capture end time
end_time = time.time()
# calculate elapsed time
elapsed_time = end_time - start_time
print ("Code execution time in seconds is ",elapsed_time)
elapsed_time_milliSeconds = elapsed_time*1000
print("code elapsed time in milliseconds is ",elapsed_time_milliSeconds)
