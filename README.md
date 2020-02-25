# CIE-A-Level-Languages-Interpreters
Interpreters for all pseudocode/fake machine code languages in the CIE A Level syllabus

## The Low-Level/Assembly Language
I called this language lcie. The source is in the Low-Level-Assembly folder. Syntax is exactly like it states in the syllabus. The only thing of note is labels. These don't need to be indented or anything, and has the syntax `name_of_label: ...`.

The way to run this is the following:
If running the executable, `lcie.exe file`
If running the python file, `lcie.py file`
It can be run with 2 flags:
  `-v` - verbose, which prints out the command that is being run and requires user input to continue running it.
