import React, {Component, Fragment} from "react";
import * as PropTypes from "prop-types";

const statusToIcon = {
  "Positive": "fa-check",
  "Inconclusive": "fa-exclamation-triangle",
  "Conclusive": "fa-bomb",
  "Unexecuted": "fa-question",
};

const statusToLabelType = {
  "Positive": "label-success",
  "Inconclusive": "label-warning",
  "Conclusive": "label-danger",
  "Unexecuted": "label-default",
};

export class StatusLabel extends Component {
  render() {
    let text = "";
    if (this.props.showText) {
      text = " " + this.props.status;
    }

    return (<div className={"label " + statusToLabelType[this.props.status]} style={{display: "flow-root"}}>
      <i className={"fa " + statusToIcon[this.props.status] + " " + this.props.size}/>{text}
    </div>);
  }
}

StatusLabel.propTypes = {status: PropTypes.string, showText: PropTypes.bool};
