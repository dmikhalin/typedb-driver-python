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
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterator, Union, Optional

from typedb.api.concept.thing.relation import Relation
from typedb.api.concept.type.role_type import RoleType
from typedb.api.concept.type.thing_type import ThingType

if TYPE_CHECKING:
    from typedb.api.connection.transaction import Transaction


class RelationType(ThingType, ABC):

    def is_relation_type(self) -> bool:
        return True

    @abstractmethod
    def create(self, transaction: Transaction) -> Relation:
        pass

    @abstractmethod
    def get_instances(self, transaction: Transaction) -> Iterator[Relation]:
        pass

    @abstractmethod
    def get_instances_explicit(self, transaction: Transaction) -> Iterator[Relation]:
        pass

    @abstractmethod
    def get_relates(self, transaction: Transaction, role_label: Optional[str] = None) \
            -> Union[Optional[RoleType], Iterator[RoleType]]:
        pass

    @abstractmethod
    def get_relates_explicit(self, transaction: Transaction) -> Iterator[RoleType]:
        pass

    @abstractmethod
    def get_relates_overridden(self, transaction: Transaction, role_label: str) -> Optional[RoleType]:
        pass

    @abstractmethod
    def set_relates(self, transaction: Transaction, role_label: str, overridden_label: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def unset_relates(self, transaction: Transaction, role_label: str) -> None:
        pass

    @abstractmethod
    def get_subtypes(self, transaction: Transaction) -> Iterator[RelationType]:
        pass

    @abstractmethod
    def set_supertype(self, transaction: Transaction, super_relation_type: RelationType) -> None:
        pass
