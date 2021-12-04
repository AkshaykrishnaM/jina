from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..document import DocumentArray
    from ...document import Document
    from ....helper import T


class ReduceMixin:
    """A mixing that provides reducing logic for :class:`DocumentArray` or :class:`DocumentArrayMemmap`"""

    def reduce(self: 'T', other: 'T') -> 'T':
        """
        Reduces other and the current DocumentArray into one DocumentArray in-place. Changes are applied to the current
        DocumentArray
        :param other: DocumentArray
        """
        for doc in other:
            if doc.id in self:
                self._reduce_doc(self[doc.id], doc)
            else:
                self.append(doc)

    @staticmethod
    def _reduce_doc(doc1: 'Document', doc2: 'Document'):
        """
        Reduces doc1 and doc2 into one Document in-place. Changes are applied to doc1
        :param doc1: first Document
        :param doc2: second Document
        """
        if len(doc2.matches) > 0:
            doc1.matches.reduce(doc2.matches)

        if len(doc2.chunks) > 0:
            doc1.chunks.reduce(doc2.chunks)

    def reduce_all(self: 'T', others: List['T']) -> 'T':
        """
        Reduces a list of DocumentArrays and this  DocumentArray into one DocumentArray. Changes are applied to this
        DocumentArray
        :param others: List of DocumentArray to be reduced
        :return: the resulting DocumentArray
        """
        for da in others:
            self.reduce(da)
        return self
