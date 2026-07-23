from astralis.memory.notes import NotesMemory

notes = NotesMemory()

notes.add_note("Buy milk")
notes.add_note("Complete DSA")

print(notes.get_notes())

notes.delete_note(1)

print(notes.get_notes())