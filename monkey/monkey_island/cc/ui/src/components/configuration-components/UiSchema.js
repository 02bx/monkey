import AdvancedMultiSelect from "../ui-components/AdvancedMultiSelect";
import PbaInput from "./PbaInput";
import {API_PBA_LINUX, API_PBA_WINDOWS} from '../pages/ConfigurePage';

export default function UiSchema(props) {
  const UiSchema = {
    basic: {
      'ui:order': ['exploiters', 'credentials'],
      exploiters: {
        exploiter_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    },
    basic_network: {},
    monkey: {
      general: {
        alive: {
          classNames: 'config-field-hidden'
        },
        post_breach_actions: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      },
      post_breach: {
        custom_PBA_linux_cmd: {
          'ui:widget': 'textarea',
          'ui:emptyValue': ''
        },
        PBA_linux_file: {
          'ui:widget': PbaInput,
          'ui:options': {
            filename: props.PBA_linux_filename,
            apiEndpoint: API_PBA_LINUX,
            setPbaFilename: props.setPbaFilenameLinux
          }
        },
        custom_PBA_windows_cmd: {
          'ui:widget': 'textarea',
          'ui:emptyValue': ''
        },
        PBA_windows_file: {
          'ui:widget': PbaInput,
          'ui:options': {
            filename: props.PBA_windows_filename,
            apiEndpoint: API_PBA_WINDOWS,
            setPbaFilename: props.setPbaFilenameWindows
          }
        },
        PBA_linux_filename: {
          classNames: 'linux-pba-file-info',
          'ui:emptyValue': ''
        },
        PBA_windows_filename: {
          classNames: 'windows-pba-file-info',
          'ui:emptyValue': ''
        }
      },
      system_info: {
        system_info_collector_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    },
    cnc: {},
    network: {},
    internal: {
      general: {
        started_on_island: {'ui:widget': 'hidden'}
      },
      classes: {
        finger_classes: {
          classNames: 'config-template-no-header',
          'ui:widget': AdvancedMultiSelect
        }
      }
    }
  }
  return UiSchema[props.selectedSection]
}
