import React from "react";

export function renderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
}

/* Function takes data gathered from system info collector and creates a
   string representation of machine from that data. */
export function renderMachineFromSystemData(data) {
    let machineStr = data['hostname'] + " ( ";
    data['ips'].forEach(function(ipInfo){
      if(typeof ipInfo === "object"){
        machineStr += ipInfo['addr'] + " ";
      } else {
         machineStr += ipInfo + " ";
      }
    });
    return machineStr + ")"
}

export const scanStatus = {
    UNSCANNED: 0,
    SCANNED: 1,
    USED: 2
};
