from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self.atom = elements[0]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.DIGIT = elements[2]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self.symbol = elements[2]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.DIGIT = elements[2]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self.DIGIT = elements[1]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self.NUMBER = elements[1]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[1-3]')
    REGEX_2 = re.compile('^[1-2]')
    REGEX_3 = re.compile('^[0-9]')
    REGEX_4 = re.compile('^[0]')
    REGEX_5 = re.compile('^[1-9]')
    REGEX_6 = re.compile('^[0-9]')
    REGEX_7 = re.compile('^[ \\t\\n\\r]')
    REGEX_8 = re.compile('^[-=#$:/\\\\.]')

    def _read_smiles(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['smiles'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_atom()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3 = self._offset
                address3 = self._read_chain()
                if address3 is FAILURE:
                    self._offset = index3
                    address3 = self._read_branch()
                    if address3 is FAILURE:
                        self._offset = index3
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode1(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['smiles'][index0] = (address0, self._offset)
        return address0

    def _read_chain(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['chain'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_bond()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2)
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_atom()
            if address2 is FAILURE:
                self._offset = index3
                index4 = self._offset
                address2 = self._read_DIGIT()
                if address2 is FAILURE:
                    self._offset = index4
                    index5, elements1 = self._offset, []
                    address3 = FAILURE
                    chunk0 = None
                    if self._offset < self._input_size:
                        chunk0 = self._input[self._offset:self._offset + 1]
                    if chunk0 == '%':
                        address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"%"')
                    if address3 is not FAILURE:
                        elements1.append(address3)
                        address4 = FAILURE
                        address4 = self._read_DIGIT()
                        if address4 is not FAILURE:
                            elements1.append(address4)
                            address5 = FAILURE
                            address5 = self._read_DIGIT()
                            if address5 is not FAILURE:
                                elements1.append(address5)
                            else:
                                elements1 = None
                                self._offset = index5
                        else:
                            elements1 = None
                            self._offset = index5
                    else:
                        elements1 = None
                        self._offset = index5
                    if elements1 is None:
                        address2 = FAILURE
                    else:
                        address2 = TreeNode2(self._input[index5:self._offset], index5, elements1)
                        self._offset = self._offset
                    if address2 is FAILURE:
                        self._offset = index4
                if address2 is FAILURE:
                    self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['chain'][index0] = (address0, self._offset)
        return address0

    def _read_branch(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['branch'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_bond()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                remaining0, index3, elements1, address4 = 1, self._offset, [], True
                while address4 is not FAILURE:
                    address4 = self._read_smiles()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements1)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address5 = FAILURE
                    chunk1 = None
                    if self._offset < self._input_size:
                        chunk1 = self._input[self._offset:self._offset + 1]
                    if chunk1 == ')':
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('")"')
                    if address5 is not FAILURE:
                        elements0.append(address5)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['branch'][index0] = (address0, self._offset)
        return address0

    def _read_atom(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['atom'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_bracket_atom()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_ALIPHATIC_ORGANIC()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_AROMATIC_ORGANIC()
                if address0 is FAILURE:
                    self._offset = index1
                    chunk0 = None
                    if self._offset < self._input_size:
                        chunk0 = self._input[self._offset:self._offset + 1]
                    if chunk0 == '*':
                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"*"')
                    if address0 is FAILURE:
                        self._offset = index1
        self._cache['atom'][index0] = (address0, self._offset)
        return address0

    def _read_bracket_atom(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['bracket_atom'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '[':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"["')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_NUMBER()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_symbol()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index3 = self._offset
                    address4 = self._read_chiral()
                    if address4 is FAILURE:
                        address4 = TreeNode(self._input[index3:index3], index3)
                        self._offset = index3
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index4 = self._offset
                        address5 = self._read_hcount()
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index4:index4], index4)
                            self._offset = index4
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index5 = self._offset
                            address6 = self._read_charge()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index5:index5], index5)
                                self._offset = index5
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index6 = self._offset
                                address7 = self._read_clazz()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index6:index6], index6)
                                    self._offset = index6
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    chunk1 = None
                                    if self._offset < self._input_size:
                                        chunk1 = self._input[self._offset:self._offset + 1]
                                    if chunk1 == ']':
                                        address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                        self._offset = self._offset + 1
                                    else:
                                        address8 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"]"')
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode3(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['bracket_atom'][index0] = (address0, self._offset)
        return address0

    def _read_symbol(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['symbol'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_ELEMENT_SYMBOLS()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_AROMATIC_SYMBOLS()
            if address0 is FAILURE:
                self._offset = index1
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 1]
                if chunk0 == '*':
                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"*"')
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['symbol'][index0] = (address0, self._offset)
        return address0

    def _read_chiral(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['chiral'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        index3 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 3]
        if chunk0 == '@TB':
            address1 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
            self._offset = self._offset + 3
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"@TB"')
        if address1 is FAILURE:
            self._offset = index3
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 3]
            if chunk1 == '@OH':
                address1 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                self._offset = self._offset + 3
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"@OH"')
            if address1 is FAILURE:
                self._offset = index3
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index4 = self._offset
            address2 = self._read_DIGIT()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index4:index4], index4)
                self._offset = index4
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_DIGIT()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode4(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            index5, elements1 = self._offset, []
            address4 = FAILURE
            chunk2 = None
            if self._offset < self._input_size:
                chunk2 = self._input[self._offset:self._offset + 3]
            if chunk2 == '@SP':
                address4 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                self._offset = self._offset + 3
            else:
                address4 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"@SP"')
            if address4 is not FAILURE:
                elements1.append(address4)
                address5 = FAILURE
                chunk3 = None
                if self._offset < self._input_size:
                    chunk3 = self._input[self._offset:self._offset + 1]
                if chunk3 is not None and Grammar.REGEX_1.search(chunk3):
                    address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address5 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[1-3]')
                if address5 is not FAILURE:
                    elements1.append(address5)
                else:
                    elements1 = None
                    self._offset = index5
            else:
                elements1 = None
                self._offset = index5
            if elements1 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index5:self._offset], index5, elements1)
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
                index6, elements2 = self._offset, []
                address6 = FAILURE
                index7 = self._offset
                chunk4 = None
                if self._offset < self._input_size:
                    chunk4 = self._input[self._offset:self._offset + 3]
                if chunk4 == '@AL':
                    address6 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                    self._offset = self._offset + 3
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"@AL"')
                if address6 is FAILURE:
                    self._offset = index7
                    chunk5 = None
                    if self._offset < self._input_size:
                        chunk5 = self._input[self._offset:self._offset + 3]
                    if chunk5 == '@TH':
                        address6 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                        self._offset = self._offset + 3
                    else:
                        address6 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"@TH"')
                    if address6 is FAILURE:
                        self._offset = index7
                if address6 is not FAILURE:
                    elements2.append(address6)
                    address7 = FAILURE
                    chunk6 = None
                    if self._offset < self._input_size:
                        chunk6 = self._input[self._offset:self._offset + 1]
                    if chunk6 is not None and Grammar.REGEX_2.search(chunk6):
                        address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address7 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[1-2]')
                    if address7 is not FAILURE:
                        elements2.append(address7)
                    else:
                        elements2 = None
                        self._offset = index6
                else:
                    elements2 = None
                    self._offset = index6
                if elements2 is None:
                    address0 = FAILURE
                else:
                    address0 = TreeNode(self._input[index6:self._offset], index6, elements2)
                    self._offset = self._offset
                if address0 is FAILURE:
                    self._offset = index1
                    chunk7 = None
                    if self._offset < self._input_size:
                        chunk7 = self._input[self._offset:self._offset + 2]
                    if chunk7 == '@@':
                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                        self._offset = self._offset + 2
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"@@"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk8 = None
                        if self._offset < self._input_size:
                            chunk8 = self._input[self._offset:self._offset + 1]
                        if chunk8 == '@':
                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"@"')
                        if address0 is FAILURE:
                            self._offset = index1
        self._cache['chiral'][index0] = (address0, self._offset)
        return address0

    def _read_hcount(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['hcount'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == 'H':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"H"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_DIGIT()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['hcount'][index0] = (address0, self._offset)
        return address0

    def _read_charge(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['charge'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '-':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"-"')
        if address1 is FAILURE:
            self._offset = index2
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 1]
            if chunk1 == '+':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"+"')
            if address1 is FAILURE:
                self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            index4, elements1 = self._offset, []
            address3 = FAILURE
            index5 = self._offset
            address3 = self._read_DIGIT()
            if address3 is FAILURE:
                address3 = TreeNode(self._input[index5:index5], index5)
                self._offset = index5
            if address3 is not FAILURE:
                elements1.append(address3)
                address4 = FAILURE
                address4 = self._read_DIGIT()
                if address4 is not FAILURE:
                    elements1.append(address4)
                else:
                    elements1 = None
                    self._offset = index4
            else:
                elements1 = None
                self._offset = index4
            if elements1 is None:
                address2 = FAILURE
            else:
                address2 = TreeNode5(self._input[index4:self._offset], index4, elements1)
                self._offset = self._offset
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3)
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['charge'][index0] = (address0, self._offset)
        return address0

    def _read_clazz(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['clazz'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == ':':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('":"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_NUMBER()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode6(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['clazz'][index0] = (address0, self._offset)
        return address0

    def _read_ALIPHATIC_ORGANIC(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ALIPHATIC_ORGANIC'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'Cl':
            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"Cl"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'Br':
                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"Br"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 == 'B':
                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"B"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == 'C':
                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"C"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 1]
                        if chunk4 == 'N':
                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"N"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == 'O':
                                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"O"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 1]
                                if chunk6 == 'S':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"S"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 1]
                                    if chunk7 == 'P':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                        self._offset = self._offset + 1
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"P"')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8 = None
                                        if self._offset < self._input_size:
                                            chunk8 = self._input[self._offset:self._offset + 1]
                                        if chunk8 == 'F':
                                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                            self._offset = self._offset + 1
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('"F"')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9 = None
                                            if self._offset < self._input_size:
                                                chunk9 = self._input[self._offset:self._offset + 1]
                                            if chunk9 == 'I':
                                                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                self._offset = self._offset + 1
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('"I"')
                                            if address0 is FAILURE:
                                                self._offset = index1
        self._cache['ALIPHATIC_ORGANIC'][index0] = (address0, self._offset)
        return address0

    def _read_ELEMENT_SYMBOLS(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ELEMENT_SYMBOLS'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_symb_1()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_symb_2()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_symb_3()
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['ELEMENT_SYMBOLS'][index0] = (address0, self._offset)
        return address0

    def _read_symb_1(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['symb_1'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'Os':
            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"Os"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'Og':
                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"Og"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 == 'O':
                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"O"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 2]
                    if chunk3 == 'Cu':
                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                        self._offset = self._offset + 2
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"Cu"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 2]
                        if chunk4 == 'Cs':
                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                            self._offset = self._offset + 2
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"Cs"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 2]
                            if chunk5 == 'Cr':
                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                self._offset = self._offset + 2
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"Cr"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 2]
                                if chunk6 == 'Co':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                    self._offset = self._offset + 2
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"Co"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 2]
                                    if chunk7 == 'Cn':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                        self._offset = self._offset + 2
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"Cn"')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8 = None
                                        if self._offset < self._input_size:
                                            chunk8 = self._input[self._offset:self._offset + 2]
                                        if chunk8 == 'Cm':
                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                            self._offset = self._offset + 2
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('"Cm"')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9 = None
                                            if self._offset < self._input_size:
                                                chunk9 = self._input[self._offset:self._offset + 2]
                                            if chunk9 == 'Cl':
                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                self._offset = self._offset + 2
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('"Cl"')
                                            if address0 is FAILURE:
                                                self._offset = index1
                                                chunk10 = None
                                                if self._offset < self._input_size:
                                                    chunk10 = self._input[self._offset:self._offset + 2]
                                                if chunk10 == 'Cf':
                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                    self._offset = self._offset + 2
                                                else:
                                                    address0 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append('"Cf"')
                                                if address0 is FAILURE:
                                                    self._offset = index1
                                                    chunk11 = None
                                                    if self._offset < self._input_size:
                                                        chunk11 = self._input[self._offset:self._offset + 2]
                                                    if chunk11 == 'Ce':
                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                        self._offset = self._offset + 2
                                                    else:
                                                        address0 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append('"Ce"')
                                                    if address0 is FAILURE:
                                                        self._offset = index1
                                                        chunk12 = None
                                                        if self._offset < self._input_size:
                                                            chunk12 = self._input[self._offset:self._offset + 2]
                                                        if chunk12 == 'Cd':
                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                            self._offset = self._offset + 2
                                                        else:
                                                            address0 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append('"Cd"')
                                                        if address0 is FAILURE:
                                                            self._offset = index1
                                                            chunk13 = None
                                                            if self._offset < self._input_size:
                                                                chunk13 = self._input[self._offset:self._offset + 2]
                                                            if chunk13 == 'Ca':
                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                self._offset = self._offset + 2
                                                            else:
                                                                address0 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append('"Ca"')
                                                            if address0 is FAILURE:
                                                                self._offset = index1
                                                                chunk14 = None
                                                                if self._offset < self._input_size:
                                                                    chunk14 = self._input[self._offset:self._offset + 1]
                                                                if chunk14 == 'C':
                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                    self._offset = self._offset + 1
                                                                else:
                                                                    address0 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append('"C"')
                                                                if address0 is FAILURE:
                                                                    self._offset = index1
                                                                    chunk15 = None
                                                                    if self._offset < self._input_size:
                                                                        chunk15 = self._input[self._offset:self._offset + 1]
                                                                    if chunk15 == 'P':
                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                        self._offset = self._offset + 1
                                                                    else:
                                                                        address0 = FAILURE
                                                                        if self._offset > self._failure:
                                                                            self._failure = self._offset
                                                                            self._expected = []
                                                                        if self._offset == self._failure:
                                                                            self._expected.append('"P"')
                                                                    if address0 is FAILURE:
                                                                        self._offset = index1
                                                                        chunk16 = None
                                                                        if self._offset < self._input_size:
                                                                            chunk16 = self._input[self._offset:self._offset + 2]
                                                                        if chunk16 == 'Np':
                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                            self._offset = self._offset + 2
                                                                        else:
                                                                            address0 = FAILURE
                                                                            if self._offset > self._failure:
                                                                                self._failure = self._offset
                                                                                self._expected = []
                                                                            if self._offset == self._failure:
                                                                                self._expected.append('"Np"')
                                                                        if address0 is FAILURE:
                                                                            self._offset = index1
                                                                            chunk17 = None
                                                                            if self._offset < self._input_size:
                                                                                chunk17 = self._input[self._offset:self._offset + 2]
                                                                            if chunk17 == 'No':
                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                self._offset = self._offset + 2
                                                                            else:
                                                                                address0 = FAILURE
                                                                                if self._offset > self._failure:
                                                                                    self._failure = self._offset
                                                                                    self._expected = []
                                                                                if self._offset == self._failure:
                                                                                    self._expected.append('"No"')
                                                                            if address0 is FAILURE:
                                                                                self._offset = index1
                                                                                chunk18 = None
                                                                                if self._offset < self._input_size:
                                                                                    chunk18 = self._input[self._offset:self._offset + 2]
                                                                                if chunk18 == 'Ni':
                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                    self._offset = self._offset + 2
                                                                                else:
                                                                                    address0 = FAILURE
                                                                                    if self._offset > self._failure:
                                                                                        self._failure = self._offset
                                                                                        self._expected = []
                                                                                    if self._offset == self._failure:
                                                                                        self._expected.append('"Ni"')
                                                                                if address0 is FAILURE:
                                                                                    self._offset = index1
                                                                                    chunk19 = None
                                                                                    if self._offset < self._input_size:
                                                                                        chunk19 = self._input[self._offset:self._offset + 2]
                                                                                    if chunk19 == 'Nh':
                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                        self._offset = self._offset + 2
                                                                                    else:
                                                                                        address0 = FAILURE
                                                                                        if self._offset > self._failure:
                                                                                            self._failure = self._offset
                                                                                            self._expected = []
                                                                                        if self._offset == self._failure:
                                                                                            self._expected.append('"Nh"')
                                                                                    if address0 is FAILURE:
                                                                                        self._offset = index1
                                                                                        chunk20 = None
                                                                                        if self._offset < self._input_size:
                                                                                            chunk20 = self._input[self._offset:self._offset + 2]
                                                                                        if chunk20 == 'Ne':
                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                            self._offset = self._offset + 2
                                                                                        else:
                                                                                            address0 = FAILURE
                                                                                            if self._offset > self._failure:
                                                                                                self._failure = self._offset
                                                                                                self._expected = []
                                                                                            if self._offset == self._failure:
                                                                                                self._expected.append('"Ne"')
                                                                                        if address0 is FAILURE:
                                                                                            self._offset = index1
                                                                                            chunk21 = None
                                                                                            if self._offset < self._input_size:
                                                                                                chunk21 = self._input[self._offset:self._offset + 2]
                                                                                            if chunk21 == 'Nd':
                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                self._offset = self._offset + 2
                                                                                            else:
                                                                                                address0 = FAILURE
                                                                                                if self._offset > self._failure:
                                                                                                    self._failure = self._offset
                                                                                                    self._expected = []
                                                                                                if self._offset == self._failure:
                                                                                                    self._expected.append('"Nd"')
                                                                                            if address0 is FAILURE:
                                                                                                self._offset = index1
                                                                                                chunk22 = None
                                                                                                if self._offset < self._input_size:
                                                                                                    chunk22 = self._input[self._offset:self._offset + 2]
                                                                                                if chunk22 == 'Nb':
                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                    self._offset = self._offset + 2
                                                                                                else:
                                                                                                    address0 = FAILURE
                                                                                                    if self._offset > self._failure:
                                                                                                        self._failure = self._offset
                                                                                                        self._expected = []
                                                                                                    if self._offset == self._failure:
                                                                                                        self._expected.append('"Nb"')
                                                                                                if address0 is FAILURE:
                                                                                                    self._offset = index1
                                                                                                    chunk23 = None
                                                                                                    if self._offset < self._input_size:
                                                                                                        chunk23 = self._input[self._offset:self._offset + 2]
                                                                                                    if chunk23 == 'Na':
                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                        self._offset = self._offset + 2
                                                                                                    else:
                                                                                                        address0 = FAILURE
                                                                                                        if self._offset > self._failure:
                                                                                                            self._failure = self._offset
                                                                                                            self._expected = []
                                                                                                        if self._offset == self._failure:
                                                                                                            self._expected.append('"Na"')
                                                                                                    if address0 is FAILURE:
                                                                                                        self._offset = index1
                                                                                                        chunk24 = None
                                                                                                        if self._offset < self._input_size:
                                                                                                            chunk24 = self._input[self._offset:self._offset + 1]
                                                                                                        if chunk24 == 'N':
                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                            self._offset = self._offset + 1
                                                                                                        else:
                                                                                                            address0 = FAILURE
                                                                                                            if self._offset > self._failure:
                                                                                                                self._failure = self._offset
                                                                                                                self._expected = []
                                                                                                            if self._offset == self._failure:
                                                                                                                self._expected.append('"N"')
                                                                                                        if address0 is FAILURE:
                                                                                                            self._offset = index1
                                                                                                            chunk25 = None
                                                                                                            if self._offset < self._input_size:
                                                                                                                chunk25 = self._input[self._offset:self._offset + 2]
                                                                                                            if chunk25 == 'Hs':
                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                self._offset = self._offset + 2
                                                                                                            else:
                                                                                                                address0 = FAILURE
                                                                                                                if self._offset > self._failure:
                                                                                                                    self._failure = self._offset
                                                                                                                    self._expected = []
                                                                                                                if self._offset == self._failure:
                                                                                                                    self._expected.append('"Hs"')
                                                                                                            if address0 is FAILURE:
                                                                                                                self._offset = index1
                                                                                                                chunk26 = None
                                                                                                                if self._offset < self._input_size:
                                                                                                                    chunk26 = self._input[self._offset:self._offset + 2]
                                                                                                                if chunk26 == 'Ho':
                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                    self._offset = self._offset + 2
                                                                                                                else:
                                                                                                                    address0 = FAILURE
                                                                                                                    if self._offset > self._failure:
                                                                                                                        self._failure = self._offset
                                                                                                                        self._expected = []
                                                                                                                    if self._offset == self._failure:
                                                                                                                        self._expected.append('"Ho"')
                                                                                                                if address0 is FAILURE:
                                                                                                                    self._offset = index1
                                                                                                                    chunk27 = None
                                                                                                                    if self._offset < self._input_size:
                                                                                                                        chunk27 = self._input[self._offset:self._offset + 2]
                                                                                                                    if chunk27 == 'Hg':
                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                        self._offset = self._offset + 2
                                                                                                                    else:
                                                                                                                        address0 = FAILURE
                                                                                                                        if self._offset > self._failure:
                                                                                                                            self._failure = self._offset
                                                                                                                            self._expected = []
                                                                                                                        if self._offset == self._failure:
                                                                                                                            self._expected.append('"Hg"')
                                                                                                                    if address0 is FAILURE:
                                                                                                                        self._offset = index1
                                                                                                                        chunk28 = None
                                                                                                                        if self._offset < self._input_size:
                                                                                                                            chunk28 = self._input[self._offset:self._offset + 2]
                                                                                                                        if chunk28 == 'Hf':
                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                            self._offset = self._offset + 2
                                                                                                                        else:
                                                                                                                            address0 = FAILURE
                                                                                                                            if self._offset > self._failure:
                                                                                                                                self._failure = self._offset
                                                                                                                                self._expected = []
                                                                                                                            if self._offset == self._failure:
                                                                                                                                self._expected.append('"Hf"')
                                                                                                                        if address0 is FAILURE:
                                                                                                                            self._offset = index1
                                                                                                                            chunk29 = None
                                                                                                                            if self._offset < self._input_size:
                                                                                                                                chunk29 = self._input[self._offset:self._offset + 2]
                                                                                                                            if chunk29 == 'He':
                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                self._offset = self._offset + 2
                                                                                                                            else:
                                                                                                                                address0 = FAILURE
                                                                                                                                if self._offset > self._failure:
                                                                                                                                    self._failure = self._offset
                                                                                                                                    self._expected = []
                                                                                                                                if self._offset == self._failure:
                                                                                                                                    self._expected.append('"He"')
                                                                                                                            if address0 is FAILURE:
                                                                                                                                self._offset = index1
                                                                                                                                chunk30 = None
                                                                                                                                if self._offset < self._input_size:
                                                                                                                                    chunk30 = self._input[self._offset:self._offset + 1]
                                                                                                                                if chunk30 == 'H':
                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                                                    self._offset = self._offset + 1
                                                                                                                                else:
                                                                                                                                    address0 = FAILURE
                                                                                                                                    if self._offset > self._failure:
                                                                                                                                        self._failure = self._offset
                                                                                                                                        self._expected = []
                                                                                                                                    if self._offset == self._failure:
                                                                                                                                        self._expected.append('"H"')
                                                                                                                                if address0 is FAILURE:
                                                                                                                                    self._offset = index1
                                                                                                                                    chunk31 = None
                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                        chunk31 = self._input[self._offset:self._offset + 2]
                                                                                                                                    if chunk31 == 'Sr':
                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                    else:
                                                                                                                                        address0 = FAILURE
                                                                                                                                        if self._offset > self._failure:
                                                                                                                                            self._failure = self._offset
                                                                                                                                            self._expected = []
                                                                                                                                        if self._offset == self._failure:
                                                                                                                                            self._expected.append('"Sr"')
                                                                                                                                    if address0 is FAILURE:
                                                                                                                                        self._offset = index1
                                                                                                                                        chunk32 = None
                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                            chunk32 = self._input[self._offset:self._offset + 2]
                                                                                                                                        if chunk32 == 'Sn':
                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                        else:
                                                                                                                                            address0 = FAILURE
                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                self._failure = self._offset
                                                                                                                                                self._expected = []
                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                self._expected.append('"Sn"')
                                                                                                                                        if address0 is FAILURE:
                                                                                                                                            self._offset = index1
                                                                                                                                            chunk33 = None
                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                chunk33 = self._input[self._offset:self._offset + 2]
                                                                                                                                            if chunk33 == 'Sm':
                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                            else:
                                                                                                                                                address0 = FAILURE
                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                    self._failure = self._offset
                                                                                                                                                    self._expected = []
                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                    self._expected.append('"Sm"')
                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                self._offset = index1
                                                                                                                                                chunk34 = None
                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                    chunk34 = self._input[self._offset:self._offset + 2]
                                                                                                                                                if chunk34 == 'Si':
                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                else:
                                                                                                                                                    address0 = FAILURE
                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                        self._failure = self._offset
                                                                                                                                                        self._expected = []
                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                        self._expected.append('"Si"')
                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                    self._offset = index1
                                                                                                                                                    chunk35 = None
                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                        chunk35 = self._input[self._offset:self._offset + 2]
                                                                                                                                                    if chunk35 == 'Sg':
                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                    else:
                                                                                                                                                        address0 = FAILURE
                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                            self._failure = self._offset
                                                                                                                                                            self._expected = []
                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                            self._expected.append('"Sg"')
                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                        self._offset = index1
                                                                                                                                                        chunk36 = None
                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                            chunk36 = self._input[self._offset:self._offset + 2]
                                                                                                                                                        if chunk36 == 'Se':
                                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                        else:
                                                                                                                                                            address0 = FAILURE
                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                self._expected = []
                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                self._expected.append('"Se"')
                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                            self._offset = index1
                                                                                                                                                            chunk37 = None
                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                chunk37 = self._input[self._offset:self._offset + 2]
                                                                                                                                                            if chunk37 == 'Sc':
                                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                            else:
                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                    self._expected = []
                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                    self._expected.append('"Sc"')
                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                self._offset = index1
                                                                                                                                                                chunk38 = None
                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                    chunk38 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                if chunk38 == 'Sb':
                                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                else:
                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                        self._expected = []
                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                        self._expected.append('"Sb"')
                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                    self._offset = index1
                                                                                                                                                                    chunk39 = None
                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                        chunk39 = self._input[self._offset:self._offset + 1]
                                                                                                                                                                    if chunk39 == 'S':
                                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                                                                                        self._offset = self._offset + 1
                                                                                                                                                                    else:
                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                            self._expected = []
                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                            self._expected.append('"S"')
                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                        self._offset = index1
        self._cache['symb_1'][index0] = (address0, self._offset)
        return address0

    def _read_symb_2(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['symb_2'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'Fr':
            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"Fr"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'Fm':
                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"Fm"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == 'Fl':
                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                    self._offset = self._offset + 2
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"Fl"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 2]
                    if chunk3 == 'Fe':
                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                        self._offset = self._offset + 2
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"Fe"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 1]
                        if chunk4 == 'F':
                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"F"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 2]
                            if chunk5 == 'Br':
                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                self._offset = self._offset + 2
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"Br"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 2]
                                if chunk6 == 'Bk':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                    self._offset = self._offset + 2
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"Bk"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 2]
                                    if chunk7 == 'Bi':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                        self._offset = self._offset + 2
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"Bi"')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8 = None
                                        if self._offset < self._input_size:
                                            chunk8 = self._input[self._offset:self._offset + 2]
                                        if chunk8 == 'Bh':
                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                            self._offset = self._offset + 2
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('"Bh"')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9 = None
                                            if self._offset < self._input_size:
                                                chunk9 = self._input[self._offset:self._offset + 2]
                                            if chunk9 == 'Be':
                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                self._offset = self._offset + 2
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('"Be"')
                                            if address0 is FAILURE:
                                                self._offset = index1
                                                chunk10 = None
                                                if self._offset < self._input_size:
                                                    chunk10 = self._input[self._offset:self._offset + 2]
                                                if chunk10 == 'Ba':
                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                    self._offset = self._offset + 2
                                                else:
                                                    address0 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append('"Ba"')
                                                if address0 is FAILURE:
                                                    self._offset = index1
                                                    chunk11 = None
                                                    if self._offset < self._input_size:
                                                        chunk11 = self._input[self._offset:self._offset + 1]
                                                    if chunk11 == 'B':
                                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                        self._offset = self._offset + 1
                                                    else:
                                                        address0 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append('"B"')
                                                    if address0 is FAILURE:
                                                        self._offset = index1
                                                        chunk12 = None
                                                        if self._offset < self._input_size:
                                                            chunk12 = self._input[self._offset:self._offset + 2]
                                                        if chunk12 == 'Kr':
                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                            self._offset = self._offset + 2
                                                        else:
                                                            address0 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append('"Kr"')
                                                        if address0 is FAILURE:
                                                            self._offset = index1
                                                            chunk13 = None
                                                            if self._offset < self._input_size:
                                                                chunk13 = self._input[self._offset:self._offset + 1]
                                                            if chunk13 == 'K':
                                                                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                self._offset = self._offset + 1
                                                            else:
                                                                address0 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append('"K"')
                                                            if address0 is FAILURE:
                                                                self._offset = index1
                                                                chunk14 = None
                                                                if self._offset < self._input_size:
                                                                    chunk14 = self._input[self._offset:self._offset + 2]
                                                                if chunk14 == 'Ir':
                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                    self._offset = self._offset + 2
                                                                else:
                                                                    address0 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append('"Ir"')
                                                                if address0 is FAILURE:
                                                                    self._offset = index1
                                                                    chunk15 = None
                                                                    if self._offset < self._input_size:
                                                                        chunk15 = self._input[self._offset:self._offset + 2]
                                                                    if chunk15 == 'In':
                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                        self._offset = self._offset + 2
                                                                    else:
                                                                        address0 = FAILURE
                                                                        if self._offset > self._failure:
                                                                            self._failure = self._offset
                                                                            self._expected = []
                                                                        if self._offset == self._failure:
                                                                            self._expected.append('"In"')
                                                                    if address0 is FAILURE:
                                                                        self._offset = index1
                                                                        chunk16 = None
                                                                        if self._offset < self._input_size:
                                                                            chunk16 = self._input[self._offset:self._offset + 1]
                                                                        if chunk16 == 'I':
                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                            self._offset = self._offset + 1
                                                                        else:
                                                                            address0 = FAILURE
                                                                            if self._offset > self._failure:
                                                                                self._failure = self._offset
                                                                                self._expected = []
                                                                            if self._offset == self._failure:
                                                                                self._expected.append('"I"')
                                                                        if address0 is FAILURE:
                                                                            self._offset = index1
                                                                            chunk17 = None
                                                                            if self._offset < self._input_size:
                                                                                chunk17 = self._input[self._offset:self._offset + 2]
                                                                            if chunk17 == 'Zr':
                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                self._offset = self._offset + 2
                                                                            else:
                                                                                address0 = FAILURE
                                                                                if self._offset > self._failure:
                                                                                    self._failure = self._offset
                                                                                    self._expected = []
                                                                                if self._offset == self._failure:
                                                                                    self._expected.append('"Zr"')
                                                                            if address0 is FAILURE:
                                                                                self._offset = index1
                                                                                chunk18 = None
                                                                                if self._offset < self._input_size:
                                                                                    chunk18 = self._input[self._offset:self._offset + 2]
                                                                                if chunk18 == 'Zn':
                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                    self._offset = self._offset + 2
                                                                                else:
                                                                                    address0 = FAILURE
                                                                                    if self._offset > self._failure:
                                                                                        self._failure = self._offset
                                                                                        self._expected = []
                                                                                    if self._offset == self._failure:
                                                                                        self._expected.append('"Zn"')
                                                                                if address0 is FAILURE:
                                                                                    self._offset = index1
                                                                                    chunk19 = None
                                                                                    if self._offset < self._input_size:
                                                                                        chunk19 = self._input[self._offset:self._offset + 2]
                                                                                    if chunk19 == 'Yb':
                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                        self._offset = self._offset + 2
                                                                                    else:
                                                                                        address0 = FAILURE
                                                                                        if self._offset > self._failure:
                                                                                            self._failure = self._offset
                                                                                            self._expected = []
                                                                                        if self._offset == self._failure:
                                                                                            self._expected.append('"Yb"')
                                                                                    if address0 is FAILURE:
                                                                                        self._offset = index1
                                                                                        chunk20 = None
                                                                                        if self._offset < self._input_size:
                                                                                            chunk20 = self._input[self._offset:self._offset + 1]
                                                                                        if chunk20 == 'Y':
                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                            self._offset = self._offset + 1
                                                                                        else:
                                                                                            address0 = FAILURE
                                                                                            if self._offset > self._failure:
                                                                                                self._failure = self._offset
                                                                                                self._expected = []
                                                                                            if self._offset == self._failure:
                                                                                                self._expected.append('"Y"')
                                                                                        if address0 is FAILURE:
                                                                                            self._offset = index1
                                                                                            chunk21 = None
                                                                                            if self._offset < self._input_size:
                                                                                                chunk21 = self._input[self._offset:self._offset + 2]
                                                                                            if chunk21 == 'Xe':
                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                self._offset = self._offset + 2
                                                                                            else:
                                                                                                address0 = FAILURE
                                                                                                if self._offset > self._failure:
                                                                                                    self._failure = self._offset
                                                                                                    self._expected = []
                                                                                                if self._offset == self._failure:
                                                                                                    self._expected.append('"Xe"')
                                                                                            if address0 is FAILURE:
                                                                                                self._offset = index1
                                                                                                chunk22 = None
                                                                                                if self._offset < self._input_size:
                                                                                                    chunk22 = self._input[self._offset:self._offset + 1]
                                                                                                if chunk22 == 'W':
                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                    self._offset = self._offset + 1
                                                                                                else:
                                                                                                    address0 = FAILURE
                                                                                                    if self._offset > self._failure:
                                                                                                        self._failure = self._offset
                                                                                                        self._expected = []
                                                                                                    if self._offset == self._failure:
                                                                                                        self._expected.append('"W"')
                                                                                                if address0 is FAILURE:
                                                                                                    self._offset = index1
                                                                                                    chunk23 = None
                                                                                                    if self._offset < self._input_size:
                                                                                                        chunk23 = self._input[self._offset:self._offset + 1]
                                                                                                    if chunk23 == 'V':
                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                        self._offset = self._offset + 1
                                                                                                    else:
                                                                                                        address0 = FAILURE
                                                                                                        if self._offset > self._failure:
                                                                                                            self._failure = self._offset
                                                                                                            self._expected = []
                                                                                                        if self._offset == self._failure:
                                                                                                            self._expected.append('"V"')
                                                                                                    if address0 is FAILURE:
                                                                                                        self._offset = index1
                                                                                                        chunk24 = None
                                                                                                        if self._offset < self._input_size:
                                                                                                            chunk24 = self._input[self._offset:self._offset + 3]
                                                                                                        if chunk24 == 'Uue':
                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                            self._offset = self._offset + 3
                                                                                                        else:
                                                                                                            address0 = FAILURE
                                                                                                            if self._offset > self._failure:
                                                                                                                self._failure = self._offset
                                                                                                                self._expected = []
                                                                                                            if self._offset == self._failure:
                                                                                                                self._expected.append('"Uue"')
                                                                                                        if address0 is FAILURE:
                                                                                                            self._offset = index1
                                                                                                            chunk25 = None
                                                                                                            if self._offset < self._input_size:
                                                                                                                chunk25 = self._input[self._offset:self._offset + 3]
                                                                                                            if chunk25 == 'Ubu':
                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                self._offset = self._offset + 3
                                                                                                            else:
                                                                                                                address0 = FAILURE
                                                                                                                if self._offset > self._failure:
                                                                                                                    self._failure = self._offset
                                                                                                                    self._expected = []
                                                                                                                if self._offset == self._failure:
                                                                                                                    self._expected.append('"Ubu"')
                                                                                                            if address0 is FAILURE:
                                                                                                                self._offset = index1
                                                                                                                chunk26 = None
                                                                                                                if self._offset < self._input_size:
                                                                                                                    chunk26 = self._input[self._offset:self._offset + 3]
                                                                                                                if chunk26 == 'Ubt':
                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                    self._offset = self._offset + 3
                                                                                                                else:
                                                                                                                    address0 = FAILURE
                                                                                                                    if self._offset > self._failure:
                                                                                                                        self._failure = self._offset
                                                                                                                        self._expected = []
                                                                                                                    if self._offset == self._failure:
                                                                                                                        self._expected.append('"Ubt"')
                                                                                                                if address0 is FAILURE:
                                                                                                                    self._offset = index1
                                                                                                                    chunk27 = None
                                                                                                                    if self._offset < self._input_size:
                                                                                                                        chunk27 = self._input[self._offset:self._offset + 3]
                                                                                                                    if chunk27 == 'Ubq':
                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                        self._offset = self._offset + 3
                                                                                                                    else:
                                                                                                                        address0 = FAILURE
                                                                                                                        if self._offset > self._failure:
                                                                                                                            self._failure = self._offset
                                                                                                                            self._expected = []
                                                                                                                        if self._offset == self._failure:
                                                                                                                            self._expected.append('"Ubq"')
                                                                                                                    if address0 is FAILURE:
                                                                                                                        self._offset = index1
                                                                                                                        chunk28 = None
                                                                                                                        if self._offset < self._input_size:
                                                                                                                            chunk28 = self._input[self._offset:self._offset + 3]
                                                                                                                        if chunk28 == 'Ubp':
                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                            self._offset = self._offset + 3
                                                                                                                        else:
                                                                                                                            address0 = FAILURE
                                                                                                                            if self._offset > self._failure:
                                                                                                                                self._failure = self._offset
                                                                                                                                self._expected = []
                                                                                                                            if self._offset == self._failure:
                                                                                                                                self._expected.append('"Ubp"')
                                                                                                                        if address0 is FAILURE:
                                                                                                                            self._offset = index1
                                                                                                                            chunk29 = None
                                                                                                                            if self._offset < self._input_size:
                                                                                                                                chunk29 = self._input[self._offset:self._offset + 3]
                                                                                                                            if chunk29 == 'Ubn':
                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                                self._offset = self._offset + 3
                                                                                                                            else:
                                                                                                                                address0 = FAILURE
                                                                                                                                if self._offset > self._failure:
                                                                                                                                    self._failure = self._offset
                                                                                                                                    self._expected = []
                                                                                                                                if self._offset == self._failure:
                                                                                                                                    self._expected.append('"Ubn"')
                                                                                                                            if address0 is FAILURE:
                                                                                                                                self._offset = index1
                                                                                                                                chunk30 = None
                                                                                                                                if self._offset < self._input_size:
                                                                                                                                    chunk30 = self._input[self._offset:self._offset + 3]
                                                                                                                                if chunk30 == 'Ubh':
                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                                    self._offset = self._offset + 3
                                                                                                                                else:
                                                                                                                                    address0 = FAILURE
                                                                                                                                    if self._offset > self._failure:
                                                                                                                                        self._failure = self._offset
                                                                                                                                        self._expected = []
                                                                                                                                    if self._offset == self._failure:
                                                                                                                                        self._expected.append('"Ubh"')
                                                                                                                                if address0 is FAILURE:
                                                                                                                                    self._offset = index1
                                                                                                                                    chunk31 = None
                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                        chunk31 = self._input[self._offset:self._offset + 3]
                                                                                                                                    if chunk31 == 'Ubb':
                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                                                                                                                                        self._offset = self._offset + 3
                                                                                                                                    else:
                                                                                                                                        address0 = FAILURE
                                                                                                                                        if self._offset > self._failure:
                                                                                                                                            self._failure = self._offset
                                                                                                                                            self._expected = []
                                                                                                                                        if self._offset == self._failure:
                                                                                                                                            self._expected.append('"Ubb"')
                                                                                                                                    if address0 is FAILURE:
                                                                                                                                        self._offset = index1
                                                                                                                                        chunk32 = None
                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                            chunk32 = self._input[self._offset:self._offset + 1]
                                                                                                                                        if chunk32 == 'U':
                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                                                                                                                            self._offset = self._offset + 1
                                                                                                                                        else:
                                                                                                                                            address0 = FAILURE
                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                self._failure = self._offset
                                                                                                                                                self._expected = []
                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                self._expected.append('"U"')
                                                                                                                                        if address0 is FAILURE:
                                                                                                                                            self._offset = index1
                                                                                                                                            chunk33 = None
                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                chunk33 = self._input[self._offset:self._offset + 2]
                                                                                                                                            if chunk33 == 'Ts':
                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                            else:
                                                                                                                                                address0 = FAILURE
                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                    self._failure = self._offset
                                                                                                                                                    self._expected = []
                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                    self._expected.append('"Ts"')
                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                self._offset = index1
                                                                                                                                                chunk34 = None
                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                    chunk34 = self._input[self._offset:self._offset + 2]
                                                                                                                                                if chunk34 == 'Tm':
                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                else:
                                                                                                                                                    address0 = FAILURE
                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                        self._failure = self._offset
                                                                                                                                                        self._expected = []
                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                        self._expected.append('"Tm"')
                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                    self._offset = index1
                                                                                                                                                    chunk35 = None
                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                        chunk35 = self._input[self._offset:self._offset + 2]
                                                                                                                                                    if chunk35 == 'Tl':
                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                    else:
                                                                                                                                                        address0 = FAILURE
                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                            self._failure = self._offset
                                                                                                                                                            self._expected = []
                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                            self._expected.append('"Tl"')
                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                        self._offset = index1
                                                                                                                                                        chunk36 = None
                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                            chunk36 = self._input[self._offset:self._offset + 2]
                                                                                                                                                        if chunk36 == 'Ti':
                                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                        else:
                                                                                                                                                            address0 = FAILURE
                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                self._expected = []
                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                self._expected.append('"Ti"')
                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                            self._offset = index1
                                                                                                                                                            chunk37 = None
                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                chunk37 = self._input[self._offset:self._offset + 2]
                                                                                                                                                            if chunk37 == 'Th':
                                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                            else:
                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                    self._expected = []
                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                    self._expected.append('"Th"')
                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                self._offset = index1
                                                                                                                                                                chunk38 = None
                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                    chunk38 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                if chunk38 == 'Te':
                                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                else:
                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                        self._expected = []
                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                        self._expected.append('"Te"')
                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                    self._offset = index1
                                                                                                                                                                    chunk39 = None
                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                        chunk39 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                    if chunk39 == 'Tc':
                                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                    else:
                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                            self._expected = []
                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                            self._expected.append('"Tc"')
                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                        self._offset = index1
                                                                                                                                                                        chunk40 = None
                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                            chunk40 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                        if chunk40 == 'Tb':
                                                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                        else:
                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                self._expected = []
                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                self._expected.append('"Tb"')
                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                            self._offset = index1
                                                                                                                                                                            chunk41 = None
                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                chunk41 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                            if chunk41 == 'Ta':
                                                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                            else:
                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                    self._expected.append('"Ta"')
                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                self._offset = index1
        self._cache['symb_2'][index0] = (address0, self._offset)
        return address0

    def _read_symb_3(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['symb_3'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'Au':
            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"Au"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'At':
                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"At"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == 'As':
                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                    self._offset = self._offset + 2
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"As"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 2]
                    if chunk3 == 'Ar':
                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                        self._offset = self._offset + 2
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"Ar"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 2]
                        if chunk4 == 'Am':
                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                            self._offset = self._offset + 2
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"Am"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 2]
                            if chunk5 == 'Al':
                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                self._offset = self._offset + 2
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"Al"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 2]
                                if chunk6 == 'Ag':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                    self._offset = self._offset + 2
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"Ag"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 2]
                                    if chunk7 == 'Ac':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                        self._offset = self._offset + 2
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"Ac"')
                                    if address0 is FAILURE:
                                        self._offset = index1
                                        chunk8 = None
                                        if self._offset < self._input_size:
                                            chunk8 = self._input[self._offset:self._offset + 2]
                                        if chunk8 == 'Ru':
                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                            self._offset = self._offset + 2
                                        else:
                                            address0 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append('"Ru"')
                                        if address0 is FAILURE:
                                            self._offset = index1
                                            chunk9 = None
                                            if self._offset < self._input_size:
                                                chunk9 = self._input[self._offset:self._offset + 2]
                                            if chunk9 == 'Rn':
                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                self._offset = self._offset + 2
                                            else:
                                                address0 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append('"Rn"')
                                            if address0 is FAILURE:
                                                self._offset = index1
                                                chunk10 = None
                                                if self._offset < self._input_size:
                                                    chunk10 = self._input[self._offset:self._offset + 2]
                                                if chunk10 == 'Rh':
                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                    self._offset = self._offset + 2
                                                else:
                                                    address0 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append('"Rh"')
                                                if address0 is FAILURE:
                                                    self._offset = index1
                                                    chunk11 = None
                                                    if self._offset < self._input_size:
                                                        chunk11 = self._input[self._offset:self._offset + 2]
                                                    if chunk11 == 'Rg':
                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                        self._offset = self._offset + 2
                                                    else:
                                                        address0 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append('"Rg"')
                                                    if address0 is FAILURE:
                                                        self._offset = index1
                                                        chunk12 = None
                                                        if self._offset < self._input_size:
                                                            chunk12 = self._input[self._offset:self._offset + 2]
                                                        if chunk12 == 'Rf':
                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                            self._offset = self._offset + 2
                                                        else:
                                                            address0 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append('"Rf"')
                                                        if address0 is FAILURE:
                                                            self._offset = index1
                                                            chunk13 = None
                                                            if self._offset < self._input_size:
                                                                chunk13 = self._input[self._offset:self._offset + 2]
                                                            if chunk13 == 'Re':
                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                self._offset = self._offset + 2
                                                            else:
                                                                address0 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append('"Re"')
                                                            if address0 is FAILURE:
                                                                self._offset = index1
                                                                chunk14 = None
                                                                if self._offset < self._input_size:
                                                                    chunk14 = self._input[self._offset:self._offset + 2]
                                                                if chunk14 == 'Rb':
                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                    self._offset = self._offset + 2
                                                                else:
                                                                    address0 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append('"Rb"')
                                                                if address0 is FAILURE:
                                                                    self._offset = index1
                                                                    chunk15 = None
                                                                    if self._offset < self._input_size:
                                                                        chunk15 = self._input[self._offset:self._offset + 2]
                                                                    if chunk15 == 'Ra':
                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                        self._offset = self._offset + 2
                                                                    else:
                                                                        address0 = FAILURE
                                                                        if self._offset > self._failure:
                                                                            self._failure = self._offset
                                                                            self._expected = []
                                                                        if self._offset == self._failure:
                                                                            self._expected.append('"Ra"')
                                                                    if address0 is FAILURE:
                                                                        self._offset = index1
                                                                        chunk16 = None
                                                                        if self._offset < self._input_size:
                                                                            chunk16 = self._input[self._offset:self._offset + 2]
                                                                        if chunk16 == 'Pu':
                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                            self._offset = self._offset + 2
                                                                        else:
                                                                            address0 = FAILURE
                                                                            if self._offset > self._failure:
                                                                                self._failure = self._offset
                                                                                self._expected = []
                                                                            if self._offset == self._failure:
                                                                                self._expected.append('"Pu"')
                                                                        if address0 is FAILURE:
                                                                            self._offset = index1
                                                                            chunk17 = None
                                                                            if self._offset < self._input_size:
                                                                                chunk17 = self._input[self._offset:self._offset + 2]
                                                                            if chunk17 == 'Pt':
                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                self._offset = self._offset + 2
                                                                            else:
                                                                                address0 = FAILURE
                                                                                if self._offset > self._failure:
                                                                                    self._failure = self._offset
                                                                                    self._expected = []
                                                                                if self._offset == self._failure:
                                                                                    self._expected.append('"Pt"')
                                                                            if address0 is FAILURE:
                                                                                self._offset = index1
                                                                                chunk18 = None
                                                                                if self._offset < self._input_size:
                                                                                    chunk18 = self._input[self._offset:self._offset + 2]
                                                                                if chunk18 == 'Pr':
                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                    self._offset = self._offset + 2
                                                                                else:
                                                                                    address0 = FAILURE
                                                                                    if self._offset > self._failure:
                                                                                        self._failure = self._offset
                                                                                        self._expected = []
                                                                                    if self._offset == self._failure:
                                                                                        self._expected.append('"Pr"')
                                                                                if address0 is FAILURE:
                                                                                    self._offset = index1
                                                                                    chunk19 = None
                                                                                    if self._offset < self._input_size:
                                                                                        chunk19 = self._input[self._offset:self._offset + 2]
                                                                                    if chunk19 == 'Po':
                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                        self._offset = self._offset + 2
                                                                                    else:
                                                                                        address0 = FAILURE
                                                                                        if self._offset > self._failure:
                                                                                            self._failure = self._offset
                                                                                            self._expected = []
                                                                                        if self._offset == self._failure:
                                                                                            self._expected.append('"Po"')
                                                                                    if address0 is FAILURE:
                                                                                        self._offset = index1
                                                                                        chunk20 = None
                                                                                        if self._offset < self._input_size:
                                                                                            chunk20 = self._input[self._offset:self._offset + 2]
                                                                                        if chunk20 == 'Pm':
                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                            self._offset = self._offset + 2
                                                                                        else:
                                                                                            address0 = FAILURE
                                                                                            if self._offset > self._failure:
                                                                                                self._failure = self._offset
                                                                                                self._expected = []
                                                                                            if self._offset == self._failure:
                                                                                                self._expected.append('"Pm"')
                                                                                        if address0 is FAILURE:
                                                                                            self._offset = index1
                                                                                            chunk21 = None
                                                                                            if self._offset < self._input_size:
                                                                                                chunk21 = self._input[self._offset:self._offset + 2]
                                                                                            if chunk21 == 'Pd':
                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                self._offset = self._offset + 2
                                                                                            else:
                                                                                                address0 = FAILURE
                                                                                                if self._offset > self._failure:
                                                                                                    self._failure = self._offset
                                                                                                    self._expected = []
                                                                                                if self._offset == self._failure:
                                                                                                    self._expected.append('"Pd"')
                                                                                            if address0 is FAILURE:
                                                                                                self._offset = index1
                                                                                                chunk22 = None
                                                                                                if self._offset < self._input_size:
                                                                                                    chunk22 = self._input[self._offset:self._offset + 2]
                                                                                                if chunk22 == 'Pb':
                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                    self._offset = self._offset + 2
                                                                                                else:
                                                                                                    address0 = FAILURE
                                                                                                    if self._offset > self._failure:
                                                                                                        self._failure = self._offset
                                                                                                        self._expected = []
                                                                                                    if self._offset == self._failure:
                                                                                                        self._expected.append('"Pb"')
                                                                                                if address0 is FAILURE:
                                                                                                    self._offset = index1
                                                                                                    chunk23 = None
                                                                                                    if self._offset < self._input_size:
                                                                                                        chunk23 = self._input[self._offset:self._offset + 2]
                                                                                                    if chunk23 == 'Pa':
                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                        self._offset = self._offset + 2
                                                                                                    else:
                                                                                                        address0 = FAILURE
                                                                                                        if self._offset > self._failure:
                                                                                                            self._failure = self._offset
                                                                                                            self._expected = []
                                                                                                        if self._offset == self._failure:
                                                                                                            self._expected.append('"Pa"')
                                                                                                    if address0 is FAILURE:
                                                                                                        self._offset = index1
                                                                                                        chunk24 = None
                                                                                                        if self._offset < self._input_size:
                                                                                                            chunk24 = self._input[self._offset:self._offset + 2]
                                                                                                        if chunk24 == 'Mt':
                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                            self._offset = self._offset + 2
                                                                                                        else:
                                                                                                            address0 = FAILURE
                                                                                                            if self._offset > self._failure:
                                                                                                                self._failure = self._offset
                                                                                                                self._expected = []
                                                                                                            if self._offset == self._failure:
                                                                                                                self._expected.append('"Mt"')
                                                                                                        if address0 is FAILURE:
                                                                                                            self._offset = index1
                                                                                                            chunk25 = None
                                                                                                            if self._offset < self._input_size:
                                                                                                                chunk25 = self._input[self._offset:self._offset + 2]
                                                                                                            if chunk25 == 'Mo':
                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                self._offset = self._offset + 2
                                                                                                            else:
                                                                                                                address0 = FAILURE
                                                                                                                if self._offset > self._failure:
                                                                                                                    self._failure = self._offset
                                                                                                                    self._expected = []
                                                                                                                if self._offset == self._failure:
                                                                                                                    self._expected.append('"Mo"')
                                                                                                            if address0 is FAILURE:
                                                                                                                self._offset = index1
                                                                                                                chunk26 = None
                                                                                                                if self._offset < self._input_size:
                                                                                                                    chunk26 = self._input[self._offset:self._offset + 2]
                                                                                                                if chunk26 == 'Mn':
                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                    self._offset = self._offset + 2
                                                                                                                else:
                                                                                                                    address0 = FAILURE
                                                                                                                    if self._offset > self._failure:
                                                                                                                        self._failure = self._offset
                                                                                                                        self._expected = []
                                                                                                                    if self._offset == self._failure:
                                                                                                                        self._expected.append('"Mn"')
                                                                                                                if address0 is FAILURE:
                                                                                                                    self._offset = index1
                                                                                                                    chunk27 = None
                                                                                                                    if self._offset < self._input_size:
                                                                                                                        chunk27 = self._input[self._offset:self._offset + 2]
                                                                                                                    if chunk27 == 'Mg':
                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                        self._offset = self._offset + 2
                                                                                                                    else:
                                                                                                                        address0 = FAILURE
                                                                                                                        if self._offset > self._failure:
                                                                                                                            self._failure = self._offset
                                                                                                                            self._expected = []
                                                                                                                        if self._offset == self._failure:
                                                                                                                            self._expected.append('"Mg"')
                                                                                                                    if address0 is FAILURE:
                                                                                                                        self._offset = index1
                                                                                                                        chunk28 = None
                                                                                                                        if self._offset < self._input_size:
                                                                                                                            chunk28 = self._input[self._offset:self._offset + 2]
                                                                                                                        if chunk28 == 'Md':
                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                            self._offset = self._offset + 2
                                                                                                                        else:
                                                                                                                            address0 = FAILURE
                                                                                                                            if self._offset > self._failure:
                                                                                                                                self._failure = self._offset
                                                                                                                                self._expected = []
                                                                                                                            if self._offset == self._failure:
                                                                                                                                self._expected.append('"Md"')
                                                                                                                        if address0 is FAILURE:
                                                                                                                            self._offset = index1
                                                                                                                            chunk29 = None
                                                                                                                            if self._offset < self._input_size:
                                                                                                                                chunk29 = self._input[self._offset:self._offset + 2]
                                                                                                                            if chunk29 == 'Mc':
                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                self._offset = self._offset + 2
                                                                                                                            else:
                                                                                                                                address0 = FAILURE
                                                                                                                                if self._offset > self._failure:
                                                                                                                                    self._failure = self._offset
                                                                                                                                    self._expected = []
                                                                                                                                if self._offset == self._failure:
                                                                                                                                    self._expected.append('"Mc"')
                                                                                                                            if address0 is FAILURE:
                                                                                                                                self._offset = index1
                                                                                                                                chunk30 = None
                                                                                                                                if self._offset < self._input_size:
                                                                                                                                    chunk30 = self._input[self._offset:self._offset + 2]
                                                                                                                                if chunk30 == 'Lv':
                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                else:
                                                                                                                                    address0 = FAILURE
                                                                                                                                    if self._offset > self._failure:
                                                                                                                                        self._failure = self._offset
                                                                                                                                        self._expected = []
                                                                                                                                    if self._offset == self._failure:
                                                                                                                                        self._expected.append('"Lv"')
                                                                                                                                if address0 is FAILURE:
                                                                                                                                    self._offset = index1
                                                                                                                                    chunk31 = None
                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                        chunk31 = self._input[self._offset:self._offset + 2]
                                                                                                                                    if chunk31 == 'Lu':
                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                    else:
                                                                                                                                        address0 = FAILURE
                                                                                                                                        if self._offset > self._failure:
                                                                                                                                            self._failure = self._offset
                                                                                                                                            self._expected = []
                                                                                                                                        if self._offset == self._failure:
                                                                                                                                            self._expected.append('"Lu"')
                                                                                                                                    if address0 is FAILURE:
                                                                                                                                        self._offset = index1
                                                                                                                                        chunk32 = None
                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                            chunk32 = self._input[self._offset:self._offset + 2]
                                                                                                                                        if chunk32 == 'Lr':
                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                        else:
                                                                                                                                            address0 = FAILURE
                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                self._failure = self._offset
                                                                                                                                                self._expected = []
                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                self._expected.append('"Lr"')
                                                                                                                                        if address0 is FAILURE:
                                                                                                                                            self._offset = index1
                                                                                                                                            chunk33 = None
                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                chunk33 = self._input[self._offset:self._offset + 2]
                                                                                                                                            if chunk33 == 'Li':
                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                            else:
                                                                                                                                                address0 = FAILURE
                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                    self._failure = self._offset
                                                                                                                                                    self._expected = []
                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                    self._expected.append('"Li"')
                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                self._offset = index1
                                                                                                                                                chunk34 = None
                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                    chunk34 = self._input[self._offset:self._offset + 2]
                                                                                                                                                if chunk34 == 'La':
                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                else:
                                                                                                                                                    address0 = FAILURE
                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                        self._failure = self._offset
                                                                                                                                                        self._expected = []
                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                        self._expected.append('"La"')
                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                    self._offset = index1
                                                                                                                                                    chunk35 = None
                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                        chunk35 = self._input[self._offset:self._offset + 2]
                                                                                                                                                    if chunk35 == 'Ge':
                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                    else:
                                                                                                                                                        address0 = FAILURE
                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                            self._failure = self._offset
                                                                                                                                                            self._expected = []
                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                            self._expected.append('"Ge"')
                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                        self._offset = index1
                                                                                                                                                        chunk36 = None
                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                            chunk36 = self._input[self._offset:self._offset + 2]
                                                                                                                                                        if chunk36 == 'Gd':
                                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                        else:
                                                                                                                                                            address0 = FAILURE
                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                self._expected = []
                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                self._expected.append('"Gd"')
                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                            self._offset = index1
                                                                                                                                                            chunk37 = None
                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                chunk37 = self._input[self._offset:self._offset + 2]
                                                                                                                                                            if chunk37 == 'Ga':
                                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                            else:
                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                    self._expected = []
                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                    self._expected.append('"Ga"')
                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                self._offset = index1
                                                                                                                                                                chunk38 = None
                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                    chunk38 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                if chunk38 == 'Eu':
                                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                else:
                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                        self._expected = []
                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                        self._expected.append('"Eu"')
                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                    self._offset = index1
                                                                                                                                                                    chunk39 = None
                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                        chunk39 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                    if chunk39 == 'Es':
                                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                    else:
                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                            self._expected = []
                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                            self._expected.append('"Es"')
                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                        self._offset = index1
                                                                                                                                                                        chunk40 = None
                                                                                                                                                                        if self._offset < self._input_size:
                                                                                                                                                                            chunk40 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                        if chunk40 == 'Er':
                                                                                                                                                                            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                            self._offset = self._offset + 2
                                                                                                                                                                        else:
                                                                                                                                                                            address0 = FAILURE
                                                                                                                                                                            if self._offset > self._failure:
                                                                                                                                                                                self._failure = self._offset
                                                                                                                                                                                self._expected = []
                                                                                                                                                                            if self._offset == self._failure:
                                                                                                                                                                                self._expected.append('"Er"')
                                                                                                                                                                        if address0 is FAILURE:
                                                                                                                                                                            self._offset = index1
                                                                                                                                                                            chunk41 = None
                                                                                                                                                                            if self._offset < self._input_size:
                                                                                                                                                                                chunk41 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                            if chunk41 == 'Dy':
                                                                                                                                                                                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                                self._offset = self._offset + 2
                                                                                                                                                                            else:
                                                                                                                                                                                address0 = FAILURE
                                                                                                                                                                                if self._offset > self._failure:
                                                                                                                                                                                    self._failure = self._offset
                                                                                                                                                                                    self._expected = []
                                                                                                                                                                                if self._offset == self._failure:
                                                                                                                                                                                    self._expected.append('"Dy"')
                                                                                                                                                                            if address0 is FAILURE:
                                                                                                                                                                                self._offset = index1
                                                                                                                                                                                chunk42 = None
                                                                                                                                                                                if self._offset < self._input_size:
                                                                                                                                                                                    chunk42 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                if chunk42 == 'Ds':
                                                                                                                                                                                    address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                                    self._offset = self._offset + 2
                                                                                                                                                                                else:
                                                                                                                                                                                    address0 = FAILURE
                                                                                                                                                                                    if self._offset > self._failure:
                                                                                                                                                                                        self._failure = self._offset
                                                                                                                                                                                        self._expected = []
                                                                                                                                                                                    if self._offset == self._failure:
                                                                                                                                                                                        self._expected.append('"Ds"')
                                                                                                                                                                                if address0 is FAILURE:
                                                                                                                                                                                    self._offset = index1
                                                                                                                                                                                    chunk43 = None
                                                                                                                                                                                    if self._offset < self._input_size:
                                                                                                                                                                                        chunk43 = self._input[self._offset:self._offset + 2]
                                                                                                                                                                                    if chunk43 == 'Db':
                                                                                                                                                                                        address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                                                                                                                                                                                        self._offset = self._offset + 2
                                                                                                                                                                                    else:
                                                                                                                                                                                        address0 = FAILURE
                                                                                                                                                                                        if self._offset > self._failure:
                                                                                                                                                                                            self._failure = self._offset
                                                                                                                                                                                            self._expected = []
                                                                                                                                                                                        if self._offset == self._failure:
                                                                                                                                                                                            self._expected.append('"Db"')
                                                                                                                                                                                    if address0 is FAILURE:
                                                                                                                                                                                        self._offset = index1
        self._cache['symb_3'][index0] = (address0, self._offset)
        return address0

    def _read_AROMATIC_SYMBOLS(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['AROMATIC_SYMBOLS'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == 'se':
            address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"se"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == 'as':
                address0 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"as"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 == 'b':
                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"b"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == 'c':
                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"c"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 1]
                        if chunk4 == 'n':
                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"n"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == 'o':
                                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"o"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 1]
                                if chunk6 == 'p':
                                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('"p"')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 1]
                                    if chunk7 == 's':
                                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                        self._offset = self._offset + 1
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('"s"')
                                    if address0 is FAILURE:
                                        self._offset = index1
        self._cache['AROMATIC_SYMBOLS'][index0] = (address0, self._offset)
        return address0

    def _read_AROMATIC_ORGANIC(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['AROMATIC_ORGANIC'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == 'b':
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"b"')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 1]
            if chunk1 == 'c':
                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"c"')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 == 'n':
                    address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"n"')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == 'o':
                        address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"o"')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 1]
                        if chunk4 == 's':
                            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"s"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == 'p':
                                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"p"')
                            if address0 is FAILURE:
                                self._offset = index1
        self._cache['AROMATIC_ORGANIC'][index0] = (address0, self._offset)
        return address0

    def _read_DIGIT(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['DIGIT'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_3.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[0-9]')
        self._cache['DIGIT'][index0] = (address0, self._offset)
        return address0

    def _read_NUMBER(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['NUMBER'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[0]')
        if address0 is FAILURE:
            self._offset = index1
            index2, elements0 = self._offset, []
            address1 = FAILURE
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 1]
            if chunk1 is not None and Grammar.REGEX_5.search(chunk1):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[1-9]')
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                remaining0, index3, elements1, address3 = 0, self._offset, [], True
                while address3 is not FAILURE:
                    chunk2 = None
                    if self._offset < self._input_size:
                        chunk2 = self._input[self._offset:self._offset + 1]
                    if chunk2 is not None and Grammar.REGEX_6.search(chunk2):
                        address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('[0-9]')
                    if address3 is not FAILURE:
                        elements1.append(address3)
                        remaining0 -= 1
                if remaining0 <= 0:
                    address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                    self._offset = self._offset
                else:
                    address2 = FAILURE
                if address2 is not FAILURE:
                    elements0.append(address2)
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index2:self._offset], index2, elements0)
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
        self._cache['NUMBER'][index0] = (address0, self._offset)
        return address0

    def _read_WS(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['WS'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_7.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[ \\t\\n\\r]')
        self._cache['WS'][index0] = (address0, self._offset)
        return address0

    def _read_bond(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['bond'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_8.search(chunk0):
            address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[-=#$:/\\\\.]')
        self._cache['bond'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_smiles()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()
