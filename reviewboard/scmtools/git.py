from reviewboard.ssh import utils as sshutils
        preamble = ''

            next_i, file_info, new_diff = self._parse_diff(i)


                if preamble:
                    file_info.data = preamble + file_info.data
                    preamble = ''

            elif new_diff:
                # We found a diff, but it was empty and has no file entry.
                # Reset the preamble.
                preamble = ''
            else:
                preamble += self.lines[i] + '\n'

            i = next_i

        """Parses out one file from a Git diff

        This will return a tuple of the next line number, the file info
        (if any), and whether or not we've found a file (even if we decided
        not to record it).
            parts = self._parse_git_diff(linenum)

            return parts[0], parts[1], True
            return linenum + 1, None, False
        empty_change = self._is_empty_change(linenum)
        empty_change_linenum = linenum + GIT_DIFF_EMPTY_CHANGESET_SIZE

        # Only show interesting empty changes. Basically, deletions.
        # It's likely a binary file if we're at this point, and so we want
        # to process the rest of it.
        if empty_change and not file_info.deleted:
            return empty_change_linenum, None

                file_info.data += self.lines[linenum] + "\n"
        next_diff_start_linenum = linenum + GIT_DIFF_EMPTY_CHANGESET_SIZE

        if next_diff_start_linenum >= len(self.lines):
            return True

        next_diff_start = self.lines[next_diff_start_linenum]
        return (line.startswith("Binary file") or