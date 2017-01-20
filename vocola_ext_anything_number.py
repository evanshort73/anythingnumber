import re

def merge_dicts(*dicts):
  result = {}
  for i in dicts:
    result.update(i)
  return result

def get_number_dicts():
  pos_digits = dict((x, i + 1) for i, x in enumerate(
    "one two three four five six seven eight nine" \
      .split()
  ))
  
  teens = dict((x, i + 10) for i, x in enumerate(
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen" \
      .split()
  ))
  tys = dict((x, 10 * i + 20) for i, x in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety" \
      .split()
  ))
  ten_to_99 = merge_dicts(
    teens,
    tys,
    dict(
      (x + " " + y, i + j) for x, i in tys.iteritems() \
        for y, j in pos_digits.iteritems() 
    )
  )
  
  pre_hundreds = merge_dicts(pos_digits, ten_to_99)
  sub_hundreds = merge_dicts(
    {"hundred" : 0},
    dict(("oh " + x, i) for x, i in pos_digits.iteritems()),
    ten_to_99
  )
  digits = merge_dicts(pos_digits, {"oh" : 0, "zero" : 0})
  
  return pre_hundreds, sub_hundreds, pos_digits, digits

def get_number_regex(pre_hundreds, sub_hundreds, pos_digits, digits):
  pre_hundred = "(" + "|".join(pre_hundreds.iterkeys()) + ")"
  sub_hundred = "(" + "|".join(sub_hundreds.iterkeys()) + ")"
  pos_digit = "(" + "|".join(pos_digits.iterkeys()) + ")"
  digit = "(" + "|".join(digits.iterkeys()) + ")"
  
  hundreds_string = "^{pre_hundred}(?: {sub_hundred})?$".format(
    pre_hundred=pre_hundred,
    sub_hundred=sub_hundred
  )
  thousands_string = "^{pre_hundred} thousand(?: {pre_hundred})?$".format(
    pre_hundred=pre_hundred,
  )
  digits_string = "^{pos_digit}(?: {digit})*$|^zero$".format(
    pos_digit=pos_digit,
    digit=digit
  )
  
  return re.compile(hundreds_string), \
    re.compile(thousands_string), \
    re.compile(digits_string), \
    re.compile(digit)

pre_hundreds, sub_hundreds, pos_digits, digits = get_number_dicts()
hundreds_regex, thousands_regex, digits_regex, digit_regex = get_number_regex(
  pre_hundreds,
  sub_hundreds,
  pos_digits,
  digits
)

def preprocess(anything):
  if anything.startswith("a hundred") or anything.startswith("a thousand"):
    return "one" + anything[1:]
  if anything == "to":
    return "two"
  if anything.startswith("to "):
    return "two " + anything[3:]
  if anything == "for":
    return "four"
  if anything.startswith("for "):
    return "four " + anything[4:]
  return anything

# Vocola function: AnythingNumber.Validate
def anything_number_validate(anything):
  something = preprocess(anything)

  return bool(
    hundreds_regex.match(something) or \
    thousands_regex.match(something) or \
    digits_regex.match(something)
  )

# Vocola function: AnythingNumber.Convert
def anything_number_convert(anything):
  result = None

  something = preprocess(anything)

  match = hundreds_regex.match(something)
  if match:
    result = pre_hundreds[match.group(1)]
    sub_hundred = match.group(2)
    if sub_hundred:
      result *= 100
      result += sub_hundreds[sub_hundred]

  match = thousands_regex.match(something)
  if match:
    result = pre_hundreds[match.group(1)] * 1000
    result += pre_hundreds.get(match.group(2), 0)

  if digits_regex.match(something):
    matches = digit_regex.findall(something)
    matching_digits = (str(digits[i]) for i in matches)
    result = int("".join(matching_digits))

  return result
