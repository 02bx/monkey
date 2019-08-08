import React from 'react';
import {Button, Col} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, { ReportTypes } from "../report-components/common/ReportHeader";
import PillarGrades from "../report-components/zerotrust/PillarGrades";
import FindingsTable from "../report-components/zerotrust/FindingsTable";
import RecommendationsStatusTable from "../report-components/zerotrust/RecommendationsStatus";

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      allMonkeysAreDead: false,
      runStarted: false
    };
  }

  render() {
    let res;
    // Todo move to componentDidMount
    this.getZeroTrustReportFromServer(res);

    const content = this.generateReportContent();

    return (
      <Col xs={12} lg={10}>
        <h1 className="page-title no-print">5. Zero Trust Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }

  generateReportContent() {
    let content;

    if (this.stillLoadingDataFromServer()) {
      content = "Still empty";
    } else {
      content = <div>
        <h2>Pillars Overview</h2>
        <PillarGrades pillars={this.state.pillars} />
        <h2>Recommendations Status</h2>
        <RecommendationsStatusTable recommendationsStatus={this.state.recommendations} />
        <h2>Findings</h2>
        <FindingsTable findings={this.state.findings} />
      </div>;
    }

    return (
      <div>
        <div className="text-center no-print" style={{marginBottom: '20px'}}>
          <Button bsSize="large" onClick={() => {
            this.print();
          }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
        </div>

        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
          <hr/>
          THIS IS THE RAW SERVER DATA
          <br/>
          PILLARS:
          <pre>{JSON.stringify(this.state.pillars, undefined, 2)}</pre>
          <br/>
          recommendations:
          <pre>{JSON.stringify(this.state.recommendations, undefined, 2)}</pre>
          <br/>
          FINDINGS:
          <pre>{JSON.stringify(this.state.findings, undefined, 2)}</pre>
        </div>
      </div>
    )
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined" || typeof this.state.pillars === "undefined" || typeof this.state.recommendations === "undefined";
  }

  print() {
    alert("unimplemented");
  }

  getZeroTrustReportFromServer() {
    let res;
    this.authFetch('/api/report/zero_trust/findings')
      .then(res => res.json())
      .then(res => {
        this.setState({
          findings: res
        });
      });
    this.authFetch('/api/report/zero_trust/recommendations')
      .then(res => res.json())
      .then(res => {
        this.setState({
          recommendations: res
        });
      });
    this.authFetch('/api/report/zero_trust/pillars')
      .then(res => res.json())
      .then(res => {
        this.setState({
          pillars: res
        });
      });
  }
}

export default ZeroTrustReportPageComponent;
