from Report.models import HardwareManagementConsole,ManagedSystem,LogicalPartition,VirtualIOServer
from HmcRestApi.utility.ExcelUtil import ExcelUtil
import io
from HmcRestApi.managed_system import ListManagedSystem
from HmcRestApi.logical_partition import ListLogicalPartition
from HmcRestApi.virtual_io_server import ListVirtualIOServer
from HmcRestApi.login_credentials import LogonRequest
def generate_report( name ):


    CPU = 0
    S_CPU = 1
    MEM = 2
    cliente = {}
    valid_state = ["running"]
    sum_total = [0.0,0.0,0.0]
    for i in ManagedSystem.objects.filter(associated_hmc=name):

        for k in LogicalPartition.objects.filter(associated_managed_system=i.id):
            if k.state in valid_state:
                kname = extract_client(k)
                if kname not in cliente:
                    cliente[kname] = [0.0,0.0,0.0]
                cliente[kname][CPU] += k.desired_processors
                cliente[kname][S_CPU] += k.desired_processing_units
                cliente[kname][MEM] += k.desired_memory
        for k in VirtualIOServer.objects.filter(associated_managed_system=i.id):
            if k.state in valid_state:
                kname = extract_client(k) + "-vio"
                if kname not in cliente:
                    cliente[kname] = [0.0,0.0,0.0]
                cliente[kname][CPU] += k.desired_processors
                cliente[kname][S_CPU] += k.desired_processing_units
                cliente[kname][MEM] += k.desired_memory

    output = io.BytesIO()
    write2excel = ExcelUtil(output)
    head_index = []
    head_column = ["DEDICATED CPU","SHARED CPU","MEMORY"]
    data_column = []
    for i in cliente.keys():
        head_index.append(i)
        data_column.append(cliente[i])
        sum_total[CPU]+= cliente[i][CPU]
        sum_total[MEM] += cliente[i][MEM]
        sum_total[S_CPU] += cliente[i][S_CPU]
    data_column.append(sum_total)
    head_index.append("Suma total")
    write2excel.add( head_index,head_column,data_column,name)
    write2excel.writeExcel()
    output.seek(0)
    xlsx_data = output.getvalue()
    return xlsx_data


def extract_client(lpar):
    domain_list = ["co", "com", "local","org"]
    name = None
    for i in lpar.name.split(".")[1:]:
        if i.strip() not in domain_list:
            name = i.strip().lower()
    return name if name is not None else "No client"

def sync_database( credentials ):
    print("entered")
    logon_obj = LogonRequest.Logon()
    resource_obj = logon_obj.LogonRequest(credentials.ip, credentials.username, credentials.password)
    if resource_obj is None:
        return False
    else:
        ip_temp = resource_obj[0]
        x_api_session = resource_obj[1]
        popullate_database(credentials.name, ip_temp, x_api_session)
        return True
    print("exited")


def popullate_database( name, ip, x_api_session ):

    managedsystem_object = ListManagedSystem.ListManagedSystem()
    object_list = managedsystem_object.list_ManagedSystem(ip, x_api_session)
    print( object_list )
    print("Start object list")
    for i in range(0, len(object_list)):

        ManagedSystem.objects.update_or_create(id=object_list[i].Metadata.Atom.AtomID.value(),
                                       name=object_list[i].SystemName.value(),
                                       machine_type=object_list[i].MachineTypeModelAndSerialNumber.MachineType.value(),
                                       model=object_list[i].MachineTypeModelAndSerialNumber.Model.value(),
                                       associated_hmc=name
                                       )

    ms_list = ManagedSystem.objects.filter(associated_hmc=name)
    for i in ms_list:

        logicalpartition_object = ListLogicalPartition.ListLogicalPartition()
        lpar_object_list = logicalpartition_object.list_LogicalPartition(ip, i.id, x_api_session)
        vios_object = ListVirtualIOServer.ListVirtualIOServer()
        vios_object_list = vios_object.list_VirtualIOServer(ip,i.id,x_api_session)
        if lpar_object_list is not None:
            for j in lpar_object_list:
                lpar_cpu = j.PartitionProcessorConfiguration.HasDedicatedProcessors.value()
                if lpar_cpu:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    print( uuidMS)
                    LogicalPartition.objects.update_or_create(id=j.PartitionUUID.value()+"-"+uuidMS[len(uuidMS)-1],
                                            name=j.PartitionName.value(),
                                            type=j.PartitionType.value(),
                                            state=j.PartitionState.value(),
                                            uuid=j.PartitionUUID.value(),
                                            associated_managed_system=uuidMS[len(uuidMS)-1],
                                            maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                            desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                            minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                            has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                            maximum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MaximumProcessors.value(),
                                            desired_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.DesiredProcessors.value(),
                                            minimum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MinimumProcessors.value(),
                                            maximum_processing_units=0,
                                            desired_processing_units=0,
                                            minimum_processing_units=0
                                            )

                else:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    #print(uuidMS)
                    LogicalPartition.objects.update_or_create(id=j.PartitionUUID.value()+"-"+uuidMS[len(uuidMS)-1],
                                            name=j.PartitionName.value(),
                                            type=j.PartitionType.value(),
                                            state=j.PartitionState.value(),
                                            uuid=j.PartitionUUID.value(),
                                            associated_managed_system=uuidMS[len(uuidMS)-1],
                                            maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                            desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                            minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                            has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                            maximum_processors=0,
                                            desired_processors=0,
                                            minimum_processors=0,
                                            maximum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MaximumProcessingUnits.value(),
                                            desired_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.DesiredProcessingUnits.value(),
                                            minimum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MinimumProcessingUnits.value()
                                            )

        if vios_object_list is not None:
            for j in vios_object_list:
                lpar_cpu = j.PartitionProcessorConfiguration.HasDedicatedProcessors.value()
                if lpar_cpu:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    print(uuidMS)
                    LogicalPartition.objects.update_or_create(id=j.PartitionUUID.value() + "-" + uuidMS[len(uuidMS) - 1],
                                                              name=j.PartitionName.value(),
                                                              type=j.PartitionType.value(),
                                                              state=j.PartitionState.value(),
                                                              uuid=j.PartitionUUID.value(),
                                                              associated_managed_system=uuidMS[len(uuidMS) - 1],
                                                              maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                                              desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                                              minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                                              has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                                              maximum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MaximumProcessors.value(),
                                                              desired_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.DesiredProcessors.value(),
                                                              minimum_processors=j.PartitionProcessorConfiguration.DedicatedProcessorConfiguration.MinimumProcessors.value(),
                                                              maximum_processing_units=0,
                                                              desired_processing_units=0,
                                                              minimum_processing_units=0
                                                              )

                else:
                    uuidMS = j.AssociatedManagedSystem.href.split('/')
                    # print(uuidMS)
                    LogicalPartition.objects.update_or_create(id=j.PartitionUUID.value() + "-" + uuidMS[len(uuidMS) - 1],
                                                              name=j.PartitionName.value(),
                                                              type=j.PartitionType.value(),
                                                              state=j.PartitionState.value(),
                                                              uuid=j.PartitionUUID.value(),
                                                              associated_managed_system=uuidMS[len(uuidMS) - 1],
                                                              maximum_memory=j.PartitionMemoryConfiguration.MaximumMemory.value(),
                                                              desired_memory=j.PartitionMemoryConfiguration.DesiredMemory.value(),
                                                              minimum_memory=j.PartitionMemoryConfiguration.MinimumMemory.value(),
                                                              has_dedicated_processors=j.PartitionProcessorConfiguration.HasDedicatedProcessors.value(),
                                                              maximum_processors=0,
                                                              desired_processors=0,
                                                              minimum_processors=0,
                                                              maximum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MaximumProcessingUnits.value(),
                                                              desired_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.DesiredProcessingUnits.value(),
                                                              minimum_processing_units=j.PartitionProcessorConfiguration.SharedProcessorConfiguration.MinimumProcessingUnits.value()
                                                              )

    """
    for i in ManagedSystem.select():
        print(i.name,i.id)

    for i in LogicalPartition.select():
        print(i.name, i.associated_managed_system)
    """