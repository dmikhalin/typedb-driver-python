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
from abc import abstractmethod, ABC
from itertools import chain
from typing import Optional, Iterator, TYPE_CHECKING, Any

from typedb.api.concept.type.thing_type import ThingType
from typedb.common.label import Label
from typedb.common.streamer import Streamer
from typedb.common.transitivity import Transitivity
from typedb.concept.type.type import _Type
from typedb.typedb_client_python import thing_type_is_root, thing_type_is_abstract, \
    thing_type_get_label, thing_type_delete, thing_type_is_deleted, thing_type_set_label, thing_type_set_abstract, \
    thing_type_unset_abstract, thing_type_set_plays, thing_type_unset_plays, thing_type_set_owns, thing_type_get_owns, \
    thing_type_get_plays, thing_type_get_owns_overridden, thing_type_unset_owns, thing_type_get_syntax, \
    thing_type_get_plays_overridden, concept_iterator_next

if TYPE_CHECKING:
    from typedb.api.concept.type.attribute_type import AttributeType
    from typedb.api.concept.value.value import ValueType
    from typedb.api.concept.type.annotation import Annotation
    from typedb.concept.thing.thing import _Thing
    from typedb.concept.type.attribute_type import _AttributeType
    from typedb.concept.type.role_type import _RoleType
    from typedb.concept.thing.thing import _Thing
    from typedb.connection.transaction import _Transaction


class _ThingType(ThingType, _Type, ABC):

    def as_thing_type(self) -> ThingType:
        return self

    def is_root(self) -> bool:
        return thing_type_is_root(self.native_object)

    def is_abstract(self) -> bool:
        return thing_type_is_abstract(self.native_object)

    def get_label(self) -> Label:
        return Label.of(thing_type_get_label(self.native_object))

    def delete(self, transaction: _Transaction) -> None:
        thing_type_delete(transaction.native_object, self.native_object)

    def is_deleted(self, transaction: _Transaction) -> bool:
        return thing_type_is_deleted(transaction.native_object, self.native_object)

    def set_label(self, transaction: _Transaction, new_label: Label) -> None:
        thing_type_set_label(transaction.native_object, self.native_object, new_label)

    @abstractmethod
    def get_instances(self, transaction: _Transaction):
        pass

    @abstractmethod
    def get_instances_explicit(self, transaction: _Transaction):
        pass

    def set_abstract(self, transaction: _Transaction) -> None:
        thing_type_set_abstract(transaction.native_object, self.native_object)

    def unset_abstract(self, transaction: _Transaction) -> None:
        thing_type_unset_abstract(transaction.native_object, self.native_object)

    def set_plays(self, transaction: _Transaction,
                  role_type: _RoleType, overridden_role_type: Optional[_RoleType] = None) -> None:
        thing_type_set_plays(transaction.native_object,
                             self.native_object, role_type.native_object,
                             overridden_role_type.native_object if overridden_role_type else None)

    def unset_plays(self, transaction: _Transaction, role_type: _RoleType) -> None:
        thing_type_unset_plays(transaction.native_object, self.native_object, role_type.native_object)

    def set_owns(self, transaction: _Transaction, attribute_type: _AttributeType,
                 overridden_type: Optional[_AttributeType] = None, annotations: Optional[set[Annotation]] = None
                 ) -> None:
        overridden_type_native = overridden_type.native_object if overridden_type else None
        annotations_array = [anno.native_object for anno in annotations] if annotations else []
        thing_type_set_owns(
            transaction.native_object,
            self.native_object,
            attribute_type.native_object,
            overridden_type_native,
            annotations_array,
        )

    def get_owns(self, transaction: _Transaction, value_type: Optional[ValueType] = None,
                 transitivity: Transitivity = Transitivity.TRANSITIVE, annotations: Optional[set[Annotation]] = None
                 ) -> Iterator[AttributeType]:
        return map(type_.attribute_type._AttributeType,
                   Streamer(thing_type_get_owns(transaction.native_object,
                                                self.native_object,
                                                value_type.native_object if value_type else None,
                                                transitivity.value,
                                                [anno.native_object for anno in annotations] if annotations else []),
                            concept_iterator_next))

    def get_owns_explicit(self, transaction: _Transaction, value_type: Optional[ValueType] = None,
                          annotations: Optional[set[Annotation]] = None):
        return self.get_owns(transaction, value_type, Transitivity.EXPLICIT, annotations)

    def get_plays(self, transaction: _Transaction, transitivity: Transitivity = Transitivity.TRANSITIVE
                  ) -> Iterator[_RoleType]:
        return map(type_.role_type._RoleType,
                   Streamer(thing_type_get_plays(transaction.native_object, self.native_object, transitivity.value),
                            concept_iterator_next))

    def get_plays_explicit(self, transaction: _Transaction) -> Iterator[_RoleType]:
        return self.get_plays(transaction, Transitivity.EXPLICIT)

    def get_plays_overridden(self, transaction: _Transaction, role_type: _RoleType) -> Optional[_RoleType]:
        from typedb.concept.type.role_type import _RoleType

        if res := thing_type_get_plays_overridden(transaction.native_object,
                                                  self.native_object, role_type.native_object):
            return _RoleType(res)
        return None

    def get_owns_overridden(self, transaction: _Transaction, attribute_type: _AttributeType) -> Optional[AttributeType]:
        if res := thing_type_get_owns_overridden(transaction.native_object,
                                                 self.native_object, attribute_type.native_object):
            return type_.attribute_type._AttributeType(res)
        return None

    def unset_owns(self, transaction: _Transaction, attribute_type: _AttributeType) -> None:
        thing_type_unset_owns(transaction.native_object,
                              self.native_object, attribute_type.native_object)

    def get_syntax(self, transaction: _Transaction) -> str:
        return thing_type_get_syntax(transaction.native_object, self.native_object, )


class _Root(_ThingType):

    ROOT_LABEL = Label.of("thing")

    def get_label(self) -> Label:
        return self.ROOT_LABEL

    def get_supertype(self, transaction: _Transaction) -> Optional[_ThingType]:
        return None

    def get_supertypes(self, transaction: _Transaction) -> Iterator[_ThingType]:
        return self,

    def get_subtypes(self, transaction: _Transaction) -> Iterator[Any]:
        return chain((self, ),
                     transaction.concepts.get_root_entity_type().get_subtypes(transaction),
                     transaction.concepts.get_root_relation_type().get_subtypes(transaction),
                     transaction.concepts.get_root_attribute_type().get_subtypes(transaction))

    def get_subtypes_explicit(self, transaction: _Transaction) -> Iterator[Any]:
        return (transaction.concepts.get_root_entity_type(),
                transaction.concepts.get_root_relation_type(),
                transaction.concepts.get_root_attribute_type())

    def get_instances(self, transaction: _Transaction) -> Iterator[Any]:
        return chain((self, ),
                     transaction.concepts.get_root_entity_type().get_instances(transaction),
                     transaction.concepts.get_root_relation_type().get_instances(transaction),
                     transaction.concepts.get_root_attribute_type().get_instances(transaction))

    def get_instances_explicit(self, transaction: _Transaction) -> Iterator[_Thing]:
        return ()
