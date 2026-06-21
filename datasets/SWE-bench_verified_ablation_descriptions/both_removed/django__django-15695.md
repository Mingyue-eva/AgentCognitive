RenameIndex() crashes when unnamed index is moving backward and forward.

RenameIndex() should restore the old auto-generated name when an unnamed index for unique_together is moving backward. Now re-applying RenameIndex() crashes.