from django.contrib.auth import get_user_model

from .ticket import (Ticket, TicketPriority,
                     TicketType, TicketStatus,
                     Work, ProblemArea)
from .spare_part import (SparePart, Condition,
                         SupplierCompany, SparePartUser)
from .service_object import (ServiceObject, CriterionType,
                             ServiceObjectModel, ServiceObjectType,
                             ServiceLevel)
from .other import (Country, Region,
                    City, Department)
from .contract import (Contract, ContractFiles,
                       ContractType, ContractStatus)
from .client import Client, CompanyType

User = get_user_model()
