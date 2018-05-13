# A small program that takes 2 inputs, then calculates the given celsius in farenheit

# Function to calculate the temperature in farenheit
def farenheit_calculator(day, celsius):
    far_calc = 1.8*celsius + 32
    print('Today is ', day)
    print('And the temperature in farenheit is ', far_calc)

    if far_calc >= 80:
        return 'It is hot and sunny'
    else:
        return ' is not hot'

print('Please type in the day following this format (yyyy-mm-dd): ')
a_day = str(input())
print('Now type in the temperature in celsius: ')
a_celsius = int(input())

a = farenheit_calculator(a_day, a_celsius)
print(a)

