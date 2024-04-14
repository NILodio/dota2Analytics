import { Button, Flex, Icon, useDisclosure, Stack, Spacer} from "@chakra-ui/react";
import { FaPlus, FaTrash, FaTrain, FaIceCream} from "react-icons/fa";
import AddUser from "../Admin/AddUser";
import AddPoll from "../Poll/Addpoll";
import DeletePolls from "../Poll/DeletePolls";
import RandomPolls from "../Poll/RandomPolls";
import PredictPolls from "../Poll/PredictPolls";

interface NavbarProps {
  type: string;
}

const Navbar = ({ type }: NavbarProps) => {
  const addUserModal = useDisclosure();
  const addPollModal = useDisclosure();
  const deletePollsModal = useDisclosure();
  const randomPollsModal = useDisclosure();
  const predictPollsModal = useDisclosure();

  const handleAddButtonClick = () => {
    if (type === "User") {
      addUserModal.onOpen();
    } else if (type === "Poll") {
      addPollModal.onOpen();
    } else {
      addUserModal.onOpen(); // Default action
    }
  };

  const handleClearButtonClick = () => {
    deletePollsModal.onOpen();
  };

  const handleRandomButtonClick = () => {
    randomPollsModal.onOpen();
  };

  const handlePredictButtonClick = () => {
    predictPollsModal.onOpen();
  };



  return (
  <Flex py={8} gap={4}>
    {type === "Poll" ? (
      <>
        <Stack direction="row" spacing={4} align="center">
          <Button
            variant="primary"
            gap={1}
            fontSize={{ base: "sm", md: "inherit" }}
            onClick={handleAddButtonClick}
          >
            <Icon as={FaPlus} /> Add {type}
          </Button>
          <Button
            variant="outline"
            gap={1}
            fontSize={{ base: "sm", md: "inherit" }}
            onClick={handleClearButtonClick}
          >
            <Icon as={FaTrash} /> Clear {type}
          </Button>
          <Button
            variant="outline"
            gap={1}
            fontSize={{ base: "sm", md: "inherit" }}
            onClick={handleRandomButtonClick}
          >
            <Icon as={FaTrain} /> Random {type}
          </Button>
          <Spacer />
        </Stack>
        <Button
          variant="primary"
          gap={2}
          fontSize={{ base: "sm", md: "inherit" }}
          onClick={handlePredictButtonClick}
        >
          <Icon as={FaIceCream} /> Predict {type}
        </Button>
      </>
    ) : (
      <Button
        variant="primary"
        gap={1}
        fontSize={{ base: "sm", md: "inherit" }}
        onClick={handleAddButtonClick}
      >
        <Icon as={FaPlus} /> Add {type}
      </Button>
    )}
    <AddUser isOpen={addUserModal.isOpen} onClose={addUserModal.onClose} />
    <AddPoll isOpen={addPollModal.isOpen} onClose={addPollModal.onClose} />
    <DeletePolls isOpen={deletePollsModal.isOpen} onClose={deletePollsModal.onClose} />
    <RandomPolls isOpen={randomPollsModal.isOpen} onClose={randomPollsModal.onClose} />
    <PredictPolls isOpen={predictPollsModal.isOpen} onClose={predictPollsModal.onClose} />
  </Flex>

  );
};

export default Navbar;
