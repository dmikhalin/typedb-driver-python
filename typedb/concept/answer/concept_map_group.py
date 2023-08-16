#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

from typedb.api.answer.concept_map_group import ConceptMapGroup
from typedb.common.exception import TypeDBClientExceptionExt, ILLEGAL_STATE, NULL_NATIVE_OBJECT
from typedb.common.iterator_wrapper import IteratorWrapper
from typedb.common.native_object_mixin import NativeObjectMixin
from typedb.concept.answer.concept_map import _ConceptMap
from typedb.concept import concept_factory

from typedb.native_client_wrapper import concept_map_group_get_owner, concept_map_group_get_concept_maps, \
    concept_map_iterator_next, concept_map_group_to_string, concept_map_group_equals

if TYPE_CHECKING:
    from typedb.api.concept.concept import Concept
    from typedb.api.answer.concept_map import ConceptMap
    from typedb.native_client_wrapper import ConceptMapGroup as NativeConceptMapGroup


class _ConceptMapGroup(ConceptMapGroup, NativeObjectMixin):

    def __init__(self, concept_map_group: NativeConceptMapGroup):
        if not concept_map_group:
            raise TypeDBClientExceptionExt(NULL_NATIVE_OBJECT)
        self.__native_object = concept_map_group

    @property
    def _native_object(self) -> NativeConceptMapGroup:
        return self.__native_object

    @property
    def _native_object_not_owned_exception(self) -> TypeDBClientExceptionExt:
        return TypeDBClientExceptionExt.of(ILLEGAL_STATE)

    def owner(self) -> Concept:
        return concept_factory.wrap_concept(concept_map_group_get_owner(self.native_object))

    def concept_maps(self) -> Iterator[ConceptMap]:
        return map(_ConceptMap, IteratorWrapper(concept_map_group_get_concept_maps(self.native_object),
                                                concept_map_iterator_next))

    def __repr__(self):
        return concept_map_group_to_string(self.native_object)

    def __eq__(self, other):
        if other is self:
            return True
        if not other or type(other) != type(self):
            return False
        return concept_map_group_equals(self.native_object, other.native_object)

    def __hash__(self):
        return hash((self.owner(), tuple(self.concept_maps())))
