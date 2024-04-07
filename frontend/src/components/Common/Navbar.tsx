import { Button, Flex, Icon, useDisclosure, Stack } from "@chakra-ui/react";
import { FaPlus, FaTrash } from "react-icons/fa";
import AddUser from "../Admin/AddUser";
import AddPoll from "../Poll/Addpoll";
import DeletePolls from "../Poll/DeletePolls";

interface NavbarProps {
  type: string;
}

const Navbar = ({ type }: NavbarProps) => {
  const addUserModal = useDisclosure();
  const addPollModal = useDisclosure();
  const deletePollsModal = useDisclosure();

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

  return (
    <Flex py={8} gap={4}>
      {type === "Poll" ? (
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
        </Stack>
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
    </Flex>
  );
};

export default Navbar;
