# schema.py
import graphene
from .resources import *

class Query(
    ClearanceQuery, ContainmentStatusQuery, DepartmentQuery, DesignationQuery,
    EmployeeQuery, EmployeeClearanceQuery, EmployeeDesignationQuery, EmployeeMedicalQuery,
    MissionQuery, OriginQuery, MissionOriginQuery, SpecimenQuery, SpecimenContainmentStatusQuery,
    SpecimenMedicalQuery, SpecimenMissionQuery, AuthQuery, DepartmentMissionQuery,
    EmployeeMissionQuery, ResearcherSpecimenQuery, ResourceQuery, ClearanceResourceAccessQuery, graphene.ObjectType):
    
    pass

class Mutation(
    ClearanceMutation, ContainmentStatusMutation, DepartmentMutation, DesignationMutation,
    EmployeeMutation, EmployeeClearanceMutation, EmployeeDesignationMutation, EmployeeMedicalMutation,
    MissionMutation, OriginMutation, MissionOriginMutation, SpecimenMutation, SpecimenContainmentStatusMutation,
    SpecimenMedicalMutation, SpecimenMissionMutation, AuthMutation, DepartmentMissionMutation,
    EmployeeMissionMutation, ResearcherSpecimenMutation, ResourceMutation, ClearanceResourceAccessMutation,
    SearchMutation, graphene.ObjectType):
    
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
