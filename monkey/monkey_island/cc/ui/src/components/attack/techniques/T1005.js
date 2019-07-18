import React from 'react';
import '../../../styles/Collapse.scss'
import ReactTable from "react-table";
import {renderMachineFromSystemData, scanStatus} from "./Helpers";

class T1005 extends React.Component {

  constructor(props) {
    super(props);
  }

  static getDataColumns() {
    return ([{
      Header: "Data gathered from local systems",
      columns: [
        {Header: 'Machine', id: 'machine', accessor: x => renderMachineFromSystemData(x.machine), style: { 'whiteSpace': 'unset' }},
        {Header: 'Type', id: 'type', accessor: x => x.type, style: { 'whiteSpace': 'unset' }},
        {Header: 'Info', id: 'info', accessor: x => x.info, style: { 'whiteSpace': 'unset' }},
        ]}])};

  render() {
    return (
      <div>
        <div>{this.props.data.message}</div>
        <br/>
        {this.props.data.status === scanStatus.USED ?
          <ReactTable
              columns={T1005.getDataColumns()}
              data={this.props.data.collected_data}
              showPagination={false}
              defaultPageSize={this.props.data.collected_data.length}
          /> : ""}
      </div>
    );
  }
}

export default T1005;
