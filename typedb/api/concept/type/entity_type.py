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
from typing import TYPE_CHECKING, Iterator

from typedb.api.concept.type.thing_type import ThingType

if TYPE_CHECKING:
    from typedb.api.concept.thing.entity import Entity
    from typedb.api.connection.transaction import Transaction


class EntityType(ThingType, ABC):

    def is_entity_type(self):
        return True

    @abstractmethod
    def create(self, transaction: Transaction) -> Entity:
        pass

    @abstractmethod
    def get_subtypes(self, transaction: Transaction) -> Iterator[EntityType]:
        pass

    @abstractmethod
    def get_subtypes_explicit(self, transaction: Transaction) -> Iterator[EntityType]:
        pass

    @abstractmethod
    def get_instances(self, transaction: Transaction) -> Iterator[Entity]:
        pass

    @abstractmethod
    def get_instances_explicit(self, transaction: Transaction) -> Iterator[Entity]:
        pass

    @abstractmethod
    def set_supertype(self, transaction: Transaction, super_entity_type: EntityType):
        pass
