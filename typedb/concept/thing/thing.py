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
from abc import ABC
from typing import TYPE_CHECKING, Iterator, Optional

from typedb.api.concept.thing.thing import Thing
from typedb.common.exception import TypeDBClientException, GET_HAS_WITH_MULTIPLE_FILTERS, UNEXPECTED_NATIVE_VALUE
from typedb.common.streamer import Streamer
from typedb.concept.concept import _Concept
from typedb.concept import thing, type as type_
from typedb.typedb_client_python import thing_get_iid, thing_get_is_inferred, thing_get_has, thing_get_relations, \
    thing_get_playing, thing_set_has, thing_unset_has, thing_delete, thing_is_deleted, concept_iterator_next, \
    concept_is_entity, concept_is_relation, concept_is_attribute

if TYPE_CHECKING:
    from typedb.api.concept.type.annotation import Annotation
    from typedb.concept.thing.attribute import _Attribute
    from typedb.concept.thing.relation import _Relation
    from typedb.concept.type.role_type import _RoleType
    from typedb.concept.type.attribute_type import _AttributeType
    from typedb.connection.transaction import _Transaction
    from typedb.typedb_client_python import Concept as NativeConcept


class _Thing(Thing, _Concept, ABC):

    @staticmethod
    def of(concept: NativeConcept) -> _Concept:
        if concept_is_entity(concept):
            return thing.entity._Entity(concept)
        elif concept_is_relation(concept):
            return thing.relation._Relation(concept)
        elif concept_is_attribute(concept):
            return thing.attribute._Attribute(concept)
        else:
            raise TypeDBClientException(UNEXPECTED_NATIVE_VALUE)

    def get_iid(self) -> str:
        return thing_get_iid(self.native_object)

    def is_inferred(self) -> bool:
        return thing_get_is_inferred(self.native_object)

    def get_has(self,
                transaction: _Transaction,
                *,
                attribute_type: Optional[_AttributeType] = None,
                attribute_types: list[_AttributeType] = (),
                annotations: set[Annotation] = frozenset()
                ) -> Iterator[_Attribute]:
        if [bool(attribute_type), bool(attribute_types), bool(annotations)].count(True) > 1:
            raise TypeDBClientException.of(GET_HAS_WITH_MULTIPLE_FILTERS)
        if attribute_type:
            attribute_types = [attribute_type]
        native_attribute_types = [type_.native_object for type_ in attribute_types]
        native_annotations = [anno.native_object for anno in annotations]
        return map(thing.attribute._Attribute,
                   Streamer(thing_get_has(transaction.native_object, self.native_object,
                                          native_attribute_types, native_annotations),
                            concept_iterator_next))

    def get_relations(self, transaction: _Transaction, *role_types: _RoleType) -> Iterator[_Relation]:
        native_role_types = [rt.native_object for rt in role_types]
        return map(thing.relation._Relation,
                   Streamer(thing_get_relations(transaction.native_object, self.native_object, native_role_types),
                            concept_iterator_next))

    def get_playing(self, transaction: _Transaction) -> Iterator[_RoleType]:
        return map(type_.role_type._RoleType,
                   Streamer(thing_get_playing(transaction.native_object, self.native_object), concept_iterator_next))

    def set_has(self, transaction: _Transaction, attribute: _Attribute) -> None:
        thing_set_has(transaction.native_object, self.native_object, attribute.native_object)

    def unset_has(self, transaction: _Transaction, attribute: _Attribute) -> None:
        thing_unset_has(transaction.native_object, self.native_object, attribute.native_object)

    def delete(self, transaction: _Transaction) -> None:
        thing_delete(transaction.native_object, self.native_object)

    def is_deleted(self, transaction: _Transaction) -> bool:
        return thing_is_deleted(transaction.native_object, self.native_object)

    def __str__(self):
        return "%s[%s:%s]" % (type(self).__name__, self.get_type().get_label(), self.get_iid())

    def __eq__(self, other):
        if other is self:
            return True
        if not other or type(self) != type(other):
            return False
        return self.get_iid() == other.get_iid()

    def __hash__(self):
        return hash(self.get_iid())
