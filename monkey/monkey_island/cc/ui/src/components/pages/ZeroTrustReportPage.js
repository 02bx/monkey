import React, {Fragment} from 'react';
import {Col, Grid, Row} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from "../report-components/common/ReportHeader";
import PillarsOverview from "../report-components/zerotrust/PillarOverview";
import FindingsTable from "../report-components/zerotrust/FindingsTable";
import SinglePillarDirectivesStatus from "../report-components/zerotrust/SinglePillarDirectivesStatus";
import MonkeysStillAliveWarning from "../report-components/common/MonkeysStillAliveWarning";
import ReportLoader from "../report-components/common/ReportLoader";
import MustRunMonkeyWarning from "../report-components/common/MustRunMonkeyWarning";
import StatusesToPillarsSummary from "../report-components/zerotrust/StatusesToPillarsSummary";
import PrintReportButton from "../report-components/common/PrintReportButton";
import {extractExecutionStatusFromServerResponse} from "../report-components/common/ExecutionStatus";
import ZeroTrustReportLegend from "../report-components/zerotrust/ReportLegend";

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      allMonkeysAreDead: false,
      runStarted: true
    };
  }

  componentDidMount() {
    this.updatePageState();
    setInterval(this.updatePageState, 8000)
  }

  updateMonkeysRunning = () => {
    return this.authFetch('/api')
      .then(res => res.json())
      .then(res => {
        this.setState(extractExecutionStatusFromServerResponse(res));
        return res;
      });
  };

  updatePageState = () => {
    this.updateMonkeysRunning().then(res => this.getZeroTrustReportFromServer(res));
  };

  render() {
    let content;
    if (this.state.runStarted) {
      content = this.generateReportContent();
    } else {
      content = <MustRunMonkeyWarning/>;
    }

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
      content = <ReportLoader loading={true}/>;
    } else {
      content = <div id="MainContentSection">
        {this.generateOverviewSection()}
        {this.generateDirectivesSection()}
        {this.generateFindingsSection()}
      </div>;
    }

    return (
      <Fragment>
        <div style={{marginBottom: '20px'}}>
          <PrintReportButton onClick={() => {print();}} />
        </div>
        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
        </div>
        <div style={{marginTop: '20px'}}>
          <PrintReportButton onClick={() => {print();}} />
        </div>
      </Fragment>
    )
  }

  generateFindingsSection() {
    return (<div id="findings-overview">
      <h2>Findings</h2>
      <p>
        Deep-dive into the details of each test, and see the explicit events and exact timestamps in which things
        happened in your network. This will enable you to match up with your SOC logs and alerts and to gain deeper
        insight as to what exactly happened during this test.
      </p>
      <FindingsTable pillarsToStatuses={this.state.pillars.pillarsToStatuses} findings={this.state.findings}/>
    </div>);
  }

  generateDirectivesSection() {
    return (<div id="directives-overview">
      <h2>Directives</h2>
      <p>
        Analyze each zero trust recommendation by pillar, and see if you've followed through with it. See test results
        to understand how the monkey tested your adherence to that recommendation.
      </p>
      {
        Object.keys(this.state.directives).map((pillar) =>
          <SinglePillarDirectivesStatus
            key={pillar}
            pillar={pillar}
            directivesStatus={this.state.directives[pillar]}
            pillarsToStatuses={this.state.pillars.pillarsToStatuses}/>
        )
      }
    </div>);
  }

  generateOverviewSection() {
    return (<div id="overview-section">
      <h2>Summary</h2>
      <Grid fluid={true}>
        <Row>
          <Col xs={6} sm={6} md={6} lg={6}>
            <MonkeysStillAliveWarning allMonkeysAreDead={this.state.allMonkeysAreDead}/>
            <p>
              Get a quick glance of the status for each of Zero Trust's seven pillars.
            </p>
          </Col>
          <Col xs={6} sm={6} md={6} lg={6}>
            <ZeroTrustReportLegend />
          </Col>
        </Row>
        <Row className="show-grid">
          <Col xs={8} sm={8} md={8} lg={8}>
            <PillarsOverview pillarsToStatuses={this.state.pillars.pillarsToStatuses}
                             grades={this.state.pillars.grades}/>
          </Col>
          <Col xs={4} sm={4} md={4} lg={4}>
            <StatusesToPillarsSummary statusesToPillars={this.state.pillars.statusesToPillars}/>
          </Col>
        </Row>
      </Grid>
    </div>);
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined" || typeof this.state.pillars === "undefined" || typeof this.state.directives === "undefined";
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
    this.authFetch('/api/report/zero_trust/directives')
      .then(res => res.json())
      .then(res => {
        this.setState({
          directives: res
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

  anyIssuesFound() {
    const severe = function(finding) {
      return (finding.status === "Conclusive" || finding.status === "Inconclusive");
    };

    return this.state.findings.some(severe);
  }
}

export default ZeroTrustReportPageComponent;
