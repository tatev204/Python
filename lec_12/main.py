import random
import time 

def create_random_file(file_name):
   with open(file_name, "w") as file:
      for _ in range(100):
        numbers=[str(random.randint(1, 100)) for _ in range(20)]
        for number in numbers:
           file.write (number + " ")
        file.write("\n")
           
def read_and_convert_to_int(file_name):
  with open(file_name, "r") as file:
    lines = file.readlines()
    integer_arrays = [list(map(int, line.split())) for line in lines]
  return integer_arrays
  
def filter_numbers_greater_than_40(integer_arrays):
  filtered_arrays = []
  for arrays in integer_arrays:
    filtred = list(filter(lambda x: x > 40, arrays))
    filtered_arrays.append(filtred)
  return filtered_arrays
 
def writed_filtered_numbers_to_file(filtered_arrays, output_file):
   with open(output_file, "w") as file:
     for array in filtered_arrays:
       line=" ".join(map(str, array))
       file.write(line + "\n")
         
def read_as_generator(file_name):
    with open(file_name, "r") as file:
     for line in file:
         yield list(map(int, line.split()))
       
def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result=func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time 
        print(f"Execution_time: { execution_time} seconds")
        return result 
    return wrapper  

@execution_time_decorator       
def main():
  create_random_file("random_numbers.txt")
  integer_arrays = read_and_convert_to_int("random_numbers.txt")
  filtered_arrays = filter_numbers_greater_than_40(integer_arrays)
  writed_filtered_numbers_to_file(filtered_arrays, "filtered_numbers.txt")
  print("Reading from filtered numpers.txt...")
  for line in read_as_generator("filtered_numbers.txt"):
   print(line)
   
if __name__=="__main__":
   main()
